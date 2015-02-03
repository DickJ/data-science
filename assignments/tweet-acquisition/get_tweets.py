__author__ = 'Rich Johnson'

import datetime
import logging
import sys

import boto
from boto.s3.key import Key
import tweepy


def main_download_tweets(*args):
    xsd_date_format = "%Y-%m-%d"
    tprl = 450 * 15 # Tweets per rate-limit
    dur = 4 # duration in rate-limits, rate-limits are 15 min cycles
    tt = tprl * dur# Total tweets to obtain

    if len(args) == 3:
        query = args[1]
        start = datetime.datetime.strptime(args[2], xsd_date_format)
        end = datetime.datetime.strptime(args[3], xsd_date_format)
    else:
        query = '#microsoft OR #mojang'  # https://github.com/tweepy/tweepy/issues/197
        start = datetime.datetime.strptime('2015-01-21', xsd_date_format)
        end = datetime.datetime.strptime('2015-01-28', xsd_date_format)

    consumer_key = "7fVQ3PzxbO1BvJDVVnVTA"
    consumer_secret = "I7t4mD9Wm8Otn17XDyj7OPjYnpDxSfJJ5zaKqGOok"
    access_token = "33349294-H5XiEy4CV5ug9htfvkJlaeUAImeYtMbOduiYWxkwF"
    access_token_secret = "d5VEsIiZzs2qoJCloqsHC0asb6mNNpXON1KAlM7vEis"

    # Below we changed OAuthHandler to AppAuthHandler and commented out the
    # setting of the access token. Using AppAuthHandler instead increases our
    # rate limits to 450 searches per 15 minutes
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    num_files = (end - start).days
    tpf = tt/num_files  # Tweets per file = Total Tweets / of files
    for st, un in date_partition(start, end): # st = start date, un = until date
        filename = ''.join(('tweets-', st.strftime(xsd_date_format, '.json')))
        tweet_file = open(filename, 'w')
        for tweet in tweepy.Cursor(api.search, query=query, since=st,
                                   until=un).items(tpf):
            tweet_file.write(tweet._json)  # TODO Is there a non-protected json output?
        tweet_file.close()


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
    dur = 4 # duration in rate-limits, rate-limits are 15 min cycles
    tt = tprl * dur  # Total tweets to obtain
    tweepy_consumer_key = "7fVQ3PzxbO1BvJDVVnVTA"
    tweepy_consumer_secret = "I7t4mD9Wm8Otn17XDyj7OPjYnpDxSfJJ5zaKqGOok"
    conn = boto.connect_s3()  # Pass AWS_KEY and AWS_SECRET_KEY if necessary
    try:
        bucket = conn.create_bucket('rich-johnson-w205-assignment2')
    except S3CreateError:
        logging.warning("main_download_tweets():Bucket exists")
    key = Key(bucket)

    if len(args) == 3:
        query = args[1]
        start = datetime.datetime.strptime(args[2], xsd_date_format)
        end = datetime.datetime.strptime(args[3], xsd_date_format)
    else:
        query = '#microsoft OR #mojang'  # https://github.com/tweepy/tweepy/issues/197
        start = datetime.datetime.strptime('2015-01-21', xsd_date_format)
        end = datetime.datetime.strptime('2015-01-28', xsd_date_format)

    # Below we changed OAuthHandler to AppAuthHandler and commented out the
    # setting of the access token. Using AppAuthHandler instead increases our
    # rate limits to 450 searches per 15 minutes
    auth = tweepy.AppAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    num_files = (end - start).days
    tpf = tt // num_files  # Tweets per file = Total Tweets / of files
    for st, un in date_partition(start, end): # st = start date, un = until date
        filename = ''.join(('tweets-', st.strftime(xsd_date_format, '.txt')))
        key.key = filename
        for tweet in tweepy.Cursor(api.search, query=query, since=st,
                                   until=un).items(tpf):
            # Does set_cont...() append or overwrite? We need to append
            key.set_contents_from_string(tweet.text.encode("utf8"))


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
    main_download_tweets_s3(sys.argv)

