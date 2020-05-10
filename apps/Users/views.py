from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
import tweepy
import os

# Create your views here.

# This view gets oauth_token and oauth_token_secret from Twitter and sends back to the front-end
class login(View):
    def get(self, request):
        # Use tweepy.OauthHAndler to get oauth_token and oauth_token_secret keys
        try:
            auth = tweepy.OAuthHandler(os.environ.get('TWEET_API_KEY'), os.environ.get('TWEET_API_SECRET'))
            auth_response = auth.get_authorization_url()
            
            if(auth.request_token['oauth_callback_confirmed'] == 'true'):
                request.session['token'] = auth.request_token['oauth_token']
                request.session['token_secret'] = auth.request_token['oauth_token_secret']

                # redirect user to Twitter login
                return HttpResponseRedirect(auth_response)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
            return JsonResponse({"status": 500})

class callback(View):
    def get(self, request):
        # Try to get oauth_token and oauth_verifier from get request
        print(request.GET)
        if('denied' in request.GET.values):
            return render(request, "denied.html",)
