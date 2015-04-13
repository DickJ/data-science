__author__ = 'Rich Johnson'
'''
This code was modified from assignment2 to store full tweets on S3 rather
than just the text of tweets.
'''

import datetime
import json
import logging
import sys
import time

import boto
from boto.s3.key import Key
import credentials
import tweepy

def main_download_tweets_s3(*args):
    """
    Downloads tweets using Tweepy and outputs them to text files stored on S3
    This function uses Tweepy App-Only Authentication to download tweets that
    are then stored in to files based on the date the tweet
    was posted. These files are stored in a bucket on Amazon S3.
    The file format for output tweets is one tweet per line in utf-8 encoding
    :param args: [1] is a query string
                 [2] is a date string in the format YYYY-MM-DD
                 [3] is a date string in the format YYYY-MM-DD
    :return: None
    """
    xsd_date_format = "%Y-%m-%d"
    tprl = 450 * 15  # Tweets per rate-limit
    dur = 1 # duration in rate-limits, rate-limits are 15 min cycles
    tt = tprl * dur  # Total tweets to obtain
    tweepy_consumer_key = credentials.TWITTER_CONSUMER_KEY
    tweepy_consumer_secret = credentials.TWITTER_CONSUMER_SECRET
    conn = boto.connect_s3()  # Pass AWS_KEY and AWS_SECRET_KEY if necessary
    try:
        bucket = conn.create_bucket('rich-johnson-w205-assignment2')
    except S3CreateError:
        logging.warning("main_download_tweets():Bucket exists")
    key = Key(bucket)

    if len(args[0]) == 4:
        query = args[0][1]
        start = datetime.datetime.strptime(args[0][2], xsd_date_format)
        end = datetime.datetime.strptime(args[0][3], xsd_date_format)
    else:
        print "No parameters given, using defaults."
        print str(len(args))
        query = '#microsoft OR #mojang'  # https://github.com/tweepy/tweepy/issues/197
        start = datetime.datetime.strptime('2015-02-19', xsd_date_format)
        end = datetime.datetime.strptime('2015-02-25', xsd_date_format)

    # Below we changed OAuthHandler to AppAuthHandler and commented out the
    # setting of the access token. Using AppAuthHandler instead increases our
    # rate limits to 450 searches per 15 minutes
    auth = tweepy.AppAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    num_files = (end - start).days
    tpf = tt / num_files  # Tweets per file = Total Tweets / of files
    for st, un in date_partition(start, end): # st = start date, un = until date
        tweet_list = []
        logging.info("Downloading tweets from %s to %s" % (start, end))
        # TODO Fix st, un string conversions, this is ugly
        for tweet in tweepy.Cursor(api.search, q=query, since=str(st).split()[0],
                                   until=str(un).split()[0]).items(tpf):
            tweet_list.append(json.dumps(tweet._json))
        filename = ''.join(('get-tweets-output/tweets-', st.strftime(
            xsd_date_format), '.json'))
        key.key = filename
        tweet_string = ",\n".join(tuple(i for i in tweet_list))  # 1
        # tweet/line
        key.set_contents_from_string(tweet_string)


def datetime_partition(start, end, duration):
    """
    Generator to yield each partition of size duration as a string.
    :param start: starting date as a datetime.datetime object
    :param end: ending date as a datetime.datetime object
    :param duration: partition size as a datetime.timedelta object
    :return: Returns a tuple of datetime.datetime objects representing start/end
    """
    current = start
    while start == current or (end - current).days > 0 or \
            ((end - current).days == 0 and (end - current).seconds > 0):
        yield (current, current+duration)
        current = current + duration


def date_partition(start, end):
    """
    A helper function for calling datetime_partition with a partition size.
    :param start: starting date as a datetime.datetime object
    :param end: ending date as a datetime.datetime object
    :return: Returns the generator function datetime_partition()
    """
    return datetime_partition(start, end, datetime.timedelta(days=1))


if __name__ == '__main__':
    #usage: python twitter_scrape.py <query> <since> <until>
    logfile = ''.join(('logs/get_tweets-', str(time.time()), '.log'))
    logging.basicConfig(filename=logfile, level=logging.INFO)

    main_download_tweets_s3(sys.argv)