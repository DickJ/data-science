__author__ = 'Rich Johnson'
"""
Write a python program to create a db called db_followers that stores all the
followers for all the users that you find in task 2.1. Then, write a program to
find the un-followed friends after a week for the top 10 users( users that have
the highest number of followers in task 2.1) since the time that you extracted
the tweets.
"""
# Standard Packages
import logging
import time
# Installed Packages
import pymongo
import tweepy
# My Packages
import credentials # my twitter and AWS credentials


def get_followers(rcol, fcol):
    """
    Takes a pymongo collection of tweets and stores followers users in a new db

    This function looks for the top 30 retweets in rcol and stores the
    followers of the users that tweeted them in fcol.

    :param rcol: A pymongo Collection of tweets to read from
    :param fcol: A pymongo Collection of users and their followers
    :return: None
    """
    tweepy_consumer_key = credentials.TWITTER_CONSUMER_KEY
    tweepy_consumer_secret = credentials.TWITTER_CONSUMER_SECRET
    auth = tweepy.AppAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    for record in rcol.find(limit=30).sort('retweet_count',
                                                pymongo.DESCENDING):
        user = record['user']['screen_name']
        logging.info("Getting followers of user %s" % (user))
        followers_list = []
        try:
            for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
                followers_list.extend(page)
                time.sleep(60)

        # The exceptions I have been able to find are either related to the
        # connection being reset, or the user being private/deleted. Below
        # the user is skipped if they are private/no longer exist, otherwise
        # an attempt is made to reset the connection. If the second
        # connection reset fails, the user is skipped and a WARNING is
        # entered to the logger
        except tweepy.TweepError as e:
            logging.warning("%s \tUser: %s" % (e, user))
            if "Not authorized." in e:
                logging.warning("\tPrivate user, or user no longer exists")
            else:
                api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                                 wait_on_rate_limit_notify=True)
                try:
                    for page in tweepy.Cursor(api.followers_ids,
                                              screen_name=user).pages():
                        followers_list.extend(page)
                        time.sleep(60)
                except tweepy.TweepError as e2:
                    logging.warning("Reconnection attempt failed. Skipping "
                                    "user %s\n\tError: $s") % (user, e2)

        mongo_dict = {"user": user, "followers": followers_list}
        logging.info("User %s has %d followers. Adding to db" % (user, len(followers_list)))
        fcol.insert(mongo_dict)


def week1():
    """
    Stores all the followers that were found for the top 30 retweets.

    :return: None
    """
    conn = pymongo.MongoClient()
    followers_db = conn['db_followers']
    followers_coll = followers_db.week1
    read_db = conn['db_tweets']
    read_coll = read_db.tweets

    get_followers(read_coll, followers_coll)


def week2():
    """
    Finds the un-followed friends a week after week1() was run for the top 10
    users since the time that the tweets (in db_tweets) were extracted.

    Initially gets all the followers of the same users from week 1 and stores
    them in a collection named week2.
    After this is complete, we create a list of the followers who un-followed
    each user in the past week, for the top 10 users (i.e. there are 10 lists
    created).
    :return: A dict of each user and the user ids of those who unfollowed them
    """
    conn = pymongo.MongoClient()
    followers_db = conn['db_followers']
    week1 = followers_db.week1
    week2 = followers_db.week2
    read_db = conn['db_tweets']
    tweets = read_db.tweets

    get_followers(tweets, week2)

    changed_followers = {}
    for tweet in tweets.find(limit=10).sort('retweet_count',
                                             pymongo.DESCENDING):
        sn = tweet['user']['screen_name']
        record_w1 = week1.find_one({"user":sn})
        record_w2 = week2.find_one({"user":sn})

        unfollowers = []
        for follower in record_w1["followers"]:
            if follower not in record_w2["followers"]:
                unfollowers.append(follower)

        changed_followers[sn] = unfollowers



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    week1()
    # time.sleep(604800)  # :-p
    # week2()