__author__ = 'rich'
'''
1.1- Write a python program to automatically store the JSON files (associated
with the #microsoft and #mojang hash tags) returned by twitter api in  a
database called db_streamT.
'''
import pymongo
import credentials
import tweepy
import sys
import os

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print sys.argv
        print "Usage: python part1-1.py <query> <since> <until> <num tweets>"
        print "\t<query> must include '+' and 'OR' between words"
        raise ValueError

    try:
        conn = pymongo.MongoClient()
        print "Connected!"
    except pymongo.errors.ConnectionFailure, e:
        print "Connection failed : %s" % e

    tweet_db = conn['db_streamT']
    tweet_coll = tweet_db.tweet_collection

    #xsd_date_format = "%Y-%m-%d"
    query = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    tt = int(sys.argv[4])
    consumer_key = credentials.TWITTER_CONSUMER_KEY
    consumer_secret = credentials.TWITTER_CONSUMER_SECRET

    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    #print "%s %s %s %s" % (query, start, end, type(tt))
    for tweet in tweepy.Cursor(api.search, q=query, since=start,
                               until=end).items(tt):
        #print tweet.text
        tweet_coll.insert(tweet._json)

