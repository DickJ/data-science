__author__ = 'rich'
'''
Write a python program to insert the chucked data tweets (of assignment 2)
that you have stored on S3 to mongoDB in a database called db_tweets.
'''

#from boto.s3.connection import S3Connection
#from boto.s3.key import Key
import boto
import json
import pymongo
import bson

#import credentials


if __name__ == '__main__':
    try:
        conn = pymongo.MongoClient()
        print "Connected!"
    except pymongo.errors.ConnectionFailure, e:
        print "Connection failed : %s" % e

    tweet_db = conn['db_tweets']
    tweet_coll = tweet_db.tweets

    tweet_bucket_name = 'rich-johnson-w205-assignment2'
    tweet_bucket_prefix = 'get-tweets-output'

    conn = boto.connect_s3()

    tweet_bucket = conn.get_bucket(tweet_bucket_name)
    json_file_keys = tweet_bucket.list(prefix=tweet_bucket_prefix)
    for key in json_file_keys:
        json_file_contents = key.get_contents_as_string()
        tweets = json_file_contents.split("\n")  # tweets are on separate lines

        # Individual load or bulk load?
        for tweet in tweets:
            tweet = tweet.rstrip(',')  # ',' is appended to the end of each json
            j = json.loads(tweet)
            tweet_coll.insert(j)