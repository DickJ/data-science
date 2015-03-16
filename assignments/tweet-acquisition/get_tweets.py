__author__ = 'Rich Johnson'

import datetime
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
    try:
        kb_inter_received = False
        xsd_date_format = "%Y-%m-%d"
        tprl = 180 * 15  # Tweets per rate-limit
        dur = 1 # duration in rate-limits, rate-limits are 15 min cycles
        tt = tprl * dur  # Total tweets to obtain
        tweepy_consumer_key = credentials.TWITTER_CONSUMER_KEY
        tweepy_consumer_secret = credentials.TWITTER_CONSUMER_SECRET
        conn = boto.connect_s3()  # Pass AWS_KEY and AWS_SECRET_KEY if necessary
        try:
            bucket = conn.create_bucket('rich-johnson-w205-assignment2-corrections')
        except boto.exception.S3CreateError:
            logging.warning("main_download_tweets():Bucket exists")
        key = Key(bucket)

        if len(args) == 3:
            query = args[1]
            start = datetime.datetime.strptime(args[2], xsd_date_format)
            end = datetime.datetime.strptime(args[3], xsd_date_format)
        else:
            query = '#microsoft OR #mojang'  # https://github.com/tweepy/tweepy/issues/197
            start = datetime.datetime.strptime('2015-03-10', xsd_date_format)
            end = datetime.datetime.strptime('2015-03-17', xsd_date_format)

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
                tweet_list.append(tweet.text.encode("utf8"))
                # Stop fetching tweets if a KeyboardInterrupt is received
                if kb_inter_received: break

            # KeyboardInterrupts are caught in the try/except block, but we will
            # delay raising the error until the current tweet is completed. The
            # tweets acquired in the most recent iteration will not be written
            # to disk.
            if kb_inter_received: raise KeyboardInterrupt
            filename = ''.join(('get-tweets-output/tweets-', st.strftime(
                xsd_date_format), '.txt'))
            key.key = filename
            tweet_string = "\n".join(tuple(i for i in tweet_list))  # 1 tweet/line
            key.set_contents_from_string(tweet_string)

    except KeyboardInterrupt:
        print "KeyboardInterrupt: Exiting cleanly."
        kb_inter_received = True


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
    logfile = ''.join(('logs/get_tweets-', str(time.time()), '.log'))
    logging.basicConfig(filename=logfile, level=logging.INFO)

    main_download_tweets_s3(sys.argv)

