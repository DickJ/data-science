__author__ = 'rich'
import tweepy
from tweepy.api import API

consumer_key = "7fVQ3PzxbO1BvJDVVnVTA";
consumer_secret = "I7t4mD9Wm8Otn17XDyj7OPjYnpDxSfJJ5zaKqGOok";
access_token = "33349294-H5XiEy4CV5ug9htfvkJlaeUAImeYtMbOduiYWxkwF";
access_token_secret = "d5VEsIiZzs2qoJCloqsHC0asb6mNNpXON1KAlM7vEis";

key = tweepy.OAuthHandler(consumer_key, consumer_secret)
key.set_access_token(access_token, access_token_secret)

api = tweepy.API(key)

me = api.
