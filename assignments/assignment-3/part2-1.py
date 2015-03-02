__author__ = 'rich'
import pymongo

if __name__ == '__main__':
    conn = pymongo.MongoClient()
    db = conn['db_tweets']
    coll = db.tweets

    for record in coll.find(limit=30).sort('retweet_count', pymongo.DESCENDING):
        print('%s (%s) retweeted %d times: %s' % (record['user']['screen_name'],
                                                  record['user']['location'],
                                                  record['retweet_count'],
                                                  record['text']))
