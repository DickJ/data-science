__author__ = 'rich'
'''
Compute the lexical diversity of the tweets stored in db_streamT and store the
results back to Mongodb. You need to create a collection with appropriate
structure for storing the results of your analysis.
'''
import pymongo
import string
import re
import nltk

def parse(line):
    """
    :param line:
    :return:
    """
    tokens = []
    words = line.split()
    for word in words:
        if not re.match("(^http)|(^@)", word):
            t = word.lower().strip(string.punctuation)
            if t != u'':
                tokens.append(t)
    return tokens


def build_tokens_list(collection):
    """
    :param collection:
    :return:
    """
    tokens = {}

    for record in collection.find():
        line = parse(record['text'])
        for word in line:
            try:
                tokens[word] += 1
            except:
                tokens[word] = 1
    return tokens


if __name__ == '__main__':
    conn = pymongo.MongoClient()
    db = conn['db_streamT']
    coll = db.tweet_collection

    #tweet_corpus_dict = build_tokens_list(coll)
    #total_tokens

    # results are stored as a new attribute in the same db
    for record in coll.find():
        tkn_tweet = parse(record['text'])
        try:
            lexdiv = float(len(set(tkn_tweet))) / len(tkn_tweet)
        except:
            lexdiv = None
        coll.update({'_id':record['_id']}, {'$set':{
            'lexical_diversity':lexdiv}}, upsert=False)
