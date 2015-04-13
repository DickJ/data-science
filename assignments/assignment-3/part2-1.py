__author__ = 'Rich Johnson'
'''
Analyze the tweets stored in db_tweets by finding the top 30 retweets as well
as their associated usernames and the locations of users.
'''
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
