__author__ = 'rich'

import bs4
from bs4 import BeautifulSoup
import json
import logging
import pymongo
import re
import threading
import time
import urllib2

def twitter_query(query, start_date=None, end_date=None, maxpages=10):
    """

    :param start_date: a string in the format YYYY-MM-DD, default None
    :param end_date: a string in the format YYYY-MM-DD, default None
    :param query: A tuple containing desired query terms
    :param maxpages: The maximum number of pages of tweets to retrieve
    :return:
    """
    pass

def parse_tweet_json(j):
    """

    Name:       data-name=
    username:   data-screen-name=
    Date(unix): data-time=
    tweet id:   data-tweet-id=
    user id:    data-user-id=
    text:       <p class="js-tweet-text tweet-lang="XX" data-aria-label-part="0">
                    ... tweet text ... </p>
    :param j: json containing a series of tweets scraped by twitter_query()
    :return: a json containing only the information we desire in a clean format
    """
    page = re.sub('\n', ' ', j['items_html'].encode('utf-8'))
    soup = BeautifulSoup(page)
    full_tweets_list = soup.find_all('li', {'class' : 'js-stream-item'})
    for full_tweet in full_tweets_list:
        try:
            id = full_tweet.div['data-tweet-id']
            sn = full_tweet.div['data-screen-name']
            text = full_tweet.div.div.next_sibling.next_sibling.p.contents
            datetime = full_tweet.div.div.next_sibling.next_sibling.div.small.a.span['data-time']  # Is this real life?
            lang = full_tweet.div.div.next_sibling.next_sibling.p['lang']
            text_list = []
            for tag in text:
                tag = tag.encode('utf-8')
                tag = re.sub(r'<.*?>', '', str(tag)).strip()
                if tag is not '':
                    text_list.append(tag)
            text = ' '.join(text_list)
            hashtags = []
            for word in text.split():
                if re.match('^#', word):
                    hashtags.append(word)
            yield {'_id': int(id), 'screen-name': sn, 'tweet-text': text,
                   'datetime': datetime, 'lang': lang, 'hashtags': hashtags}
        except KeyError as e:
            logging.warning("Attribute %s does not exist. Skipping" % (e,))


def twitter_query(start_date, end_date, coll):
    """

    :param start_date:
    :param end_date:
    :param coll: a mongodb collection
    :return:
    """
    logging.info("Scraping tweets for %s" % (start_date,))
    MAXDEPTH = 1000
    query = (
        'https://twitter.com/search?q=%23WorldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A',
        '%20until%3A', '&src=typd')
    scroll = (
        "https://twitter.com/i/search/timeline?q=%23worldCup%20OR%20%23Brazil2014%20OR%20%23ARG%20OR%20%23GER%20since%3A",
        "%20until%3A",
        "&src=typd&include_available_features=1&include_entities=1&last_note_ts=",
        "&scroll_cursor=")

    q = query[0] + start_date + query[1] + end_date + query[2]
    try:
        start = urllib2.urlopen(q)
        start_html = start.read()
    except urllib2.URLError:
        logging.debug("%s could not be opened. Retrying in 5s" % (q,))
        time.sleep(5)
        try:
            start = urllib2.urlopen(q)
            start_html = start.read()
        except urllib2.URLError:
            logging.warning("Second attempt to open %s failed. Shutting down" % (q,))
    try:
        refr_key = re.search('data-scroll-cursor="([\w-]+)"', start_html).group(1)
        logging.info("%s successfully made initial query" % (start_date,))
    except AttributeError:
        logging.debug("twitter_query(%s, %s) where q=%s" % (start_date, end_date, q))
        logging.warning("%s can't start. Crying" % (start_date,))
        with open("logs/" + start_date + ".html", "w") as fp:
            fp.write(start_html)
        return 1


    for i in range(MAXDEPTH):
        logging.info("%s is getting page %d" % (start_date, i))
        j = scroll[0] + start_date + scroll[1] + end_date + scroll[2] + str(i) + scroll[3] + refr_key
        try:
            nxt = urllib2.urlopen(j)
            nxt_r = nxt.read()
            nj = json.loads(nxt_r)
            refr_key = nj['scroll_cursor']
            for clean_tweet in parse_tweet_json(nj):
                try:
                    coll.insert(clean_tweet)
                except pymongo.errors.DuplicateKeyError as e:
                    logging.debug(e)
            time.sleep(1)
        except urllib2.HTTPError as e:
            logging.warning("%s received error %s. Exiting" % (start_date, e))
            logging.debug("query: %s" (j,))
            logging.info("sleeping 10 min")
            time.sleep(600)
            return 1
        #except Exception as e:
        #    logging.warning("General exception: %s" % (e,))
        #    logging.debug("date: %s\tquery: %s" % (start_date, j))
        #    return 1
    logging.info("%s completed scrape." % (start_date, ))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # This could have been automated, but I was typing while thinking about
    # other aspects of this project and simply typed it all out and don't feel
    # like re-writing it to generate all these dates since they are already
    # present here.
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

    conn = pymongo.MongoClient()
    db = conn.assignment4
    coll = db.tweets

    # Range is len(dates) - 1 because the last date, 15 July, did not have any
    # world cup matches and is simply used as a stop date.
    for i in range(len(dates) - 1):
    #for i in range(2):
        thread = threading.Thread(target=twitter_query,
                                  args=(dates[i], dates[i + 1], coll))
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


nj['items_html'] contains all the html ... then it must be parsed


"""