import sys
import tweepy
import datetime
import urllib
import signal
import json

import threading
import Queue


def controlling_thread(interrupt):
    """
    Controls the termination of the program

    This function controls the termination of the program by accepting any
    input to signal the program should terminate. This signal can be any string
    and will be passed to the other thread via a Queue.

    :param interrupt: Queue to pass a kill signal to the thread getting tweets
    :return: None
    """
    a = raw_input("Enter anything to end: ")
    interrupt.put(a)


def get_tweets_thread(interrupt, query):
    """

    :param interrupt:
    :param query:
    :return:
    """

    consumer_key = "7fVQ3PzxbO1BvJDVVnVTA";
    consumer_secret = "I7t4mD9Wm8Otn17XDyj7OPjYnpDxSfJJ5zaKqGOok";
    access_token = "33349294-H5XiEy4CV5ug9htfvkJlaeUAImeYtMbOduiYWxkwF";
    access_token_secret = "d5VEsIiZzs2qoJCloqsHC0asb6mNNpXON1KAlM7vEis";

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    q = urllib.quote_plus(query)  # URL encoded query

    # Additional query parameters:
    #   since: {date}
    #   until: {date}
    # Just add them to the 'q' variable: q+" since: 2014-01-01 until: 2014-01-02"
    outfile = ''.join((query, ".json"))

    output = open(outfile, 'w')
    while interrupt.empty():
        for tweet in tweepy.Cursor(api.search, q=q).items(200):
            # FYI: JSON is in tweet._json
            output.write(str(tweet._json))
            output.write("\n")
            #print(tweet._json)
    output.close()


if __name__ == '__main__':
    word = 'jilted'
    interrupt_queue = Queue.Queue()

    #thread2 = threading.Thread(target=get_tweets_thread, args=(
    # interrupt_queue, sys.argv[1]))
    thread = threading.Thread(target=get_tweets_thread, args=(
        interrupt_queue, word) )
    thread.daemon = True
    thread.start()

    a = raw_input("Enter anything to end: ")
    interrupt_queue.put(a)

    thread.join()