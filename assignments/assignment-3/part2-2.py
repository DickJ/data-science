__author__ = 'Rich Johnson'
'''
Compute the lexical diversity of the tweets stored in db_streamT and store the
results back to Mongodb. You need to create a collection with appropriate
structure for storing the results of your analysis.
'''
import pymongo
import re
import string
import matplotlib.pyplot as plt


def parse(line):
    """
    Strips unwanted items from a tweet and returns a list of words in the tweet

    :param line: a string containing the text of a tweet
    :return: a cleaned list containing each word in the tweet
    """
    tokens = []
    words = line.split()
    for word in words:
        if not re.match("(^http)|(^@)", word):
            t = word.lower().strip(string.punctuation)
            # Because we strip punctuation above, we may be left with empty
            # strings that need not be included.
            if t != u'':
                tokens.append(t)
    return tokens


def generate_plot(ls):
    """
    Plots a histogram of the list ls

    :param ls: A list of floats to be plotted on a histogram
    :return: None
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)

    numBins = 25
    ax.hist(ls,numBins,color='green',alpha=0.8)
    plt.show()


if __name__ == '__main__':
    conn = pymongo.MongoClient()
    db = conn['db_streamT']
    coll = db.tweet_collection

    lds = []
    for record in coll.find():
        tkn_tweet = parse(record['text'])
        try:
            lexdiv = float(len(set(tkn_tweet))) / len(tkn_tweet)
            lds.append(lexdiv)
        except:
            lexdiv = None
            lds.append(0)
        # results are stored as a new attribute in the same db
        coll.update({'_id':record['_id']}, {'$set':{
            'lexical_diversity':lexdiv}}, upsert=False)

    generate_plot(lds)
