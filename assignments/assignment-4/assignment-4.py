__author__ = 'rich'

import json
import logging
import re
import threading
import time
import urllib2

def twitter_query(start_date=None, end_date=None, query, maxpages=10):
    """

    :param start_date: a string in the format YYYY-MM-DD, default None
    :param end_date: a string in the format YYYY-MM-DD, default None
    :param query: A tuple containing desired query terms
    :param maxpages: The maximum number of pages of tweets to retrieve
    :return:
    """
    pass

def parse_tweet_file_json(file):
    """

    Name:       data-name=
    username:   data-screen-name=
    Date(unix): data-time=
    tweet id:   data-tweet-id=
    user id:    data-user-id=
    text:       <p class="js-tweet-text tweet-lang="XX" data-aria-label-part="0">
                    ... tweet text ... </p>
    :param file: a file pointer to twitter_query's json responses
    :return:
    """
    json.loads(file)


def twitter_query(start_date, end_date):
    """

    :param start_date:
    :param end_date:
    :return:
    """
    logging.info("Scraping tweets for %s" % (start_date,))
    MAXDEPTH = 10000
    query = (
        'https://twitter.com/search?q=%23WorldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A',
        '%20until%3A', '&src=typd')
    scroll = (
        "https://twitter.com/i/search/timeline?q=%23worldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A",
        "%20until%3A",
        "&src=typd&include_available_features=1&include_entities=1&last_note_ts=",
        "&scroll_cursor=")

    q = query[0] + start_date + query[1] + end_date + query[2]
    start = urllib2.urlopen(q)
    start_html = start.read()
    try:
        refr_key = re.search('data-scroll-cursor="([\w-]+)"', start_html).group(1)
        logging.info("%s successfully made initial query" % (start_date,))
    except AttributeError:
        logging.debug("twitter_query(%s, %s) where q=%s" % (start_date, end_date, q))
        logging.warning("%s can't start. Crying" % (start_date,))
        with open("logs/" + start_date + ".html", "w") as fp:
            fp.write(start_html)
        return 1

    with open("tweets/worldcuptweets-" + start_date + ".json", "w") as fp:
        for i in range(MAXDEPTH):
            logging.info("%s is getting page %d" % (start_date, i))
            j = scroll[0] + start_date + scroll[1] + end_date + scroll[2] + str(i) + scroll[3] + refr_key
            try:
                nxt = urllib2.urlopen(j)
                nxt_r = nxt.read()
                nj = json.loads(nxt_r)
                refr_key = nj['scroll_cursor']
                fp.write(nxt_r)
                time.sleep(1)
            except urllib2.HTTPError as e:
                logging.warning("%s received error %s. Exiting" % (start_date, e))
                logging.debug("query: %s" (j,))
                logging.info("sleeping 10 min")
                time.sleep(600)
                return 1
            except Exception as e:
                logging.warning("General exception: %s" % (e,))
                logging.debug("date: %s\tquery: %s" (start_date, j))
                return 1
    logging.info("%s completed scrape." % (start_date, ))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    dates = ("2014-06-06", "2014-06-07", "2014-06-08", "2014-06-09",
             "2014-06-10", "2014-06-11", "2014-06-12", "2014-06-13",
             "2014-06-14", "2014-06-15", "2014-06-16", "2014-06-17",
             "2014-06-18", "2014-06-19", "2014-06-20", "2014-06-21",
             "2014-06-22", "2014-06-23", "2014-06-24", "2014-06-25",
             "2014-06-26", "2014-06-27", "2014-06-28", "2014-06-29",
             "2014-06-30", "2014-07-01", "2014-07-02", "2014-07-03",
             "2014-07-04", "2014-07-05", "2014-07-06", "2014-07-07",
             "2014-07-08", "2014-07-09", "2014-07-10", "2014-07-11",
             "2014-07-12", "2014-07-13", "2014-07-14", "2014-07-15")

    for i in range(len(dates) - 1):
        thread = threading.Thread(target=twitter_query,
                                  args=(dates[i], dates[i + 1]))
        thread.daemon = True
        try:
            thread.start()
        except Exception as e:
            logging.warning(e)

    logging.info("%d threads created." % (len(dates) - 1,))
    for i in range(len(dates) - 1):
        # noinspection PyUnboundLocalVariable
        thread.join()
        logging.info("Thread %d joined." % (i,))

"""
query = 'https://twitter.com/search?q=%23WorldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A
2014-06-06
%20until%3A
2014-07-14
&src=typd'


MAXDEPTH = 1000000
start = urllib2.urlopen(query)
start_html = start.read()
refr_key = re.search('data-scroll-cursor="([\w-]+)"', start_html).group(1)

# Multiprocess, shard
for i in range(MAXDEPTH):
    print i
    j = "https://twitter.com/i/search/timeline?q=%23worldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A2014-06-06%20until%3A2014-07-14&src=typd&include_available_features=1&include_entities=1&last_note_ts="+str(i)+"&scroll_cursor="+refr_key
    try:
        nxt = urllib2.urlopen(j)
        nxt_r = nxt.read()
        nj = json.loads(nxt_r)
        refr_key = nj['scroll_cursor']

        Needs a better storage mechanism ... i//10000 ?

        with open("tweets/worldcuptweets-"+str(i)+'.json', 'w') as fp:
            fp.write(nxt_r)
    except urllib2.HTTPError:
        time.sleep(60)
"""