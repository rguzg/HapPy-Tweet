"""HappyTweet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.Users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.twitter_login.as_view(), name='login'),
    path('callback/', user_views.callback.as_view(), name='callback'),
    path('', user_views.home.as_view(), name='home'),
    path('logout', user_views.twitter_logout.as_view(), name='logout'),
    path('api/user', user_views.get_user_data.as_view(), name='api_user'),
    path('api/classifier', user_views.read_classifiers_api.as_view(), name='read_api_classifier'),
    path('api/classifier/create', user_views.write_classifiers_api.as_view(), name='write_api_classifier'),
    path('api/tweets/<str:language>/<int:tweet_page>', user_views.user_tweets.as_view(), name='user_tweets'),
]
