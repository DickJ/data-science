__author__ = 'rich'
"""
Write a python program to create a db called db_followers that stores all the
followers for all the users that you find in task 2.1. Then, write a program to
find the un-followed friends after a week for the top 10 users( users that have
the highest number of followers in task 2.1) since the time that you extracted
the tweets.
"""
import pymongo
import tweepy
import credentials
import json
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    conn = pymongo.MongoClient()
    followers_db = conn['db_followers']
    followers_coll = followers_db.week1
    read_db = conn['db_tweets']
    read_coll = read_db.tweets

    tweepy_consumer_key = credentials.TWITTER_CONSUMER_KEY
    tweepy_consumer_secret = credentials.TWITTER_CONSUMER_SECRET
    auth = tweepy.AppAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    for record in read_coll.find(limit=30).sort('retweet_count',
                                                pymongo.DESCENDING):
        user = record['user']['screen_name']
        logging.info("Getting followers of user %s" % (user))
        followers_list = []
        try:
            for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
                followers_list.extend(page)
                # print("%s follows %s" % (follower._json['screen_name'], user))
        except tweepy.TweepError as e:  # Reconnect if we disconnected
            logging.warning(e)
            api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
            for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
                followers_list.extend(page)



        mongo_dict = {"user": user, "followers": followers_list}
        logging.info("User %s has %d followers. Adding to db" % (user, len(followers_list)))
        followers_coll.insert(mongo_dict)
