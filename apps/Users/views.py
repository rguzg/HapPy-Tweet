import os
import pickle
import json
import tweepy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from textblob import TextBlob

from apps.Users.models import Classifier
from apps.Users.models import User as user_model
from apps.Users.serializers import (read_classifier_serializer,
                                    write_classifier_serializer)

# Create your views here.

# This view requests oauth_token and oauth_token_secret from Twitter and sends back to the Twitter approve application page
class twitter_login(View):
    def get(self, request):
        # Use tweepy.OauthHAndler to get oauth_token and oauth_token_secret keys
        try:
            # Build auth object
            auth = tweepy.OAuthHandler(os.environ.get('TWEET_API_KEY'), os.environ.get('TWEET_API_SECRET'))
            auth_response = auth.get_authorization_url()
            
            if(auth.request_token['oauth_callback_confirmed'] == 'true'):
                # Save on session data for later use
                request.session['token'] = auth.request_token['oauth_token']
                request.session['token_secret'] = auth.request_token['oauth_token_secret']

                # redirect user to Twitter approval page
                return HttpResponseRedirect(auth_response)
        # Throw error and redirect to error page if couldn't get authorization URL
        except tweepy.TweepError:
            return render(request, "denied.html",)

# This view is called when user approves the application on Twitter. It requests an access token, saves user data on db and logs the user in
class callback(View):
    def get(self, request):
        # Try to get oauth_token and oauth_verifier from get request

        if('denied' in request.GET):
            return render(request, "denied.html",)
        # Check that the oauth_token in the GET request is the same as the saved token
        if(request.GET['oauth_token'] == request.session.get('token')):
            # Rebuild auth object
            auth = tweepy.OAuthHandler(os.environ.get('TWEET_API_KEY'), os.environ.get('TWEET_API_SECRET'))
            token = request.session.get('token')
            auth.request_token = { 'oauth_token' : token, 'oauth_token_secret' : request.GET['oauth_verifier'] }

            # Request access_token from Twitter
            try:
                auth.get_access_token(request.GET['oauth_verifier'])

                # Save on session data for later use
                request.session['token'] = auth.access_token
                request.session['token_secret'] = auth.access_token_secret
                print(auth.access_token_secret)
            except tweepy.TweepError:
                return render(request, "denied.html",)
  
            # Check that user doesn't exist on user db
            verifyUser = user_model.objects.filter(username=request.session.get('token')).first()
            if(verifyUser is None):
                verifyUser = user_model.objects.create_user(username=request.session.get('token'), password=request.session.get('token_secret'))
                
                api = tweepy.API(auth)
                credentials = api.verify_credentials()
                    
                # Save user information on user db
                verifyUser.twitter_id = credentials._json['id_str']
                verifyUser.save()
                
            # Login user
            usuario = authenticate(username=request.session['token'], password=request.session['token_secret'])
            login(request, usuario)

            return HttpResponseRedirect('/')
        # In case someone makes a GET request manually
        else:
            return HttpResponseRedirect('/')
                    
# This view redirects the user to the login template or to the HapPy Tweet template, depending on whether the user is logged in or not
class home(View):
    def get(self, request):
        if request.user.is_authenticated:
            # Get number of classifiers to display on template:
            all_classifiers = Classifier.objects.all()
            classifier_name = []

            for classifier in all_classifiers:
                classifier_name.append(classifier.name)

            context = {'classifiers': classifier_name}
            return render(request, 'home.html', context)
        else:
            return render(request, 'login.html')

class user_tweets(View):
    def get(self, request, language, tweet_page):
        twitter_api = get_tweetpy_object(request)
        
        # Get classifier object for selected language. Each classifier might run on a separate process in the future, so that a new object doesn't have to be created everytime the function is called
        classifier = get_object_or_404(Classifier, name=language)

        with open('Classifiers/{0}'.format(classifier.location), 'rb') as input:
            opened_classifier = pickle.load(input)
        # Get tweets from Twitter API
        # This aproach will lead to repeated tweets, but you're running out of time m8
        tweets = []
        # tweets = twitter_api.home_timeline(page=tweet_page)
        tweets_array = []
        
        for tweet in tweets:
            # Check that a tweet is in the solicited language:
            if(tweet._json['lang'] == classifier.shortened_name):
                # Check sentiment of tweet
                sentiment = TextBlob(tweet._json['text'], classifier=opened_classifier).classify()
                if(sentiment == 'pos'):
                    serialized_tweet = {}
                    serialized_tweet['tweet_id'] = tweet._json['id_str']

                    serialized_tweet['text'] = tweet._json['text']

                    tweets_array.append(serialized_tweet)
        example = open('example.json', 'r', encoding='utf-8').read()
        return JsonResponse(json.loads(example), safe=False)
        # return JsonResponse(tweets_array, safe=False)

# Logs user out
class twitter_logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

# Gets user data from Twitter API
@method_decorator(login_required, name='dispatch')
class get_user_data(View):

    def get(self, request):
        api = get_tweetpy_object(request)
        credentials = api.verify_credentials()

        user_data = {
            'name': credentials._json['name'], 
            'screen_name': credentials._json['screen_name'],
            'profile_image_url': credentials._json['profile_image_url'],
            'profile_banner_url': credentials._json['profile_banner_url']
            }

        return JsonResponse(user_data)

# Rest API read-only endpoint for classfiers
@method_decorator(csrf_exempt, name='dispatch')
class read_classifiers_api(ListAPIView):
    queryset = Classifier.objects.all()
    serializer_class = read_classifier_serializer

# Rest API endpoint to specify new classfiers
@method_decorator(csrf_exempt, name='dispatch')
class write_classifiers_api(CreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Classifier.objects.all()
    serializer_class = write_classifier_serializer

# Returns a tweetpy object ready to make API calls to
def get_tweetpy_object(request):
    # Rebuild auth object 
    auth = tweepy.OAuthHandler(os.environ.get('TWEET_API_KEY'), os.environ.get('TWEET_API_SECRET'))
    auth.set_access_token(request.session['token'], request.session['token_secret'])

    return tweepy.API(auth)
