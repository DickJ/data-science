__author__ = 'rich'
import nltk
from nltk.corpus import inaugural
import math

def tf(t, d):
    count = 0
    dw = d.lower().split(' ')
    for word in dw:
        if word == t:
            count += 1
    try:
        rv = float(count) / len(dw)
    except ZeroDivisionError:
        rv = 1
    return rv

def idf(term, corpus):
    count = 0
    for doc in corpus:
        if term.lower() in doc.lower():
            count += 1
    return math.log(1 + float(len(corpus)) / count)


if __name__ == '__main__':
    q = ['fellow', 'citizens']
    corpus = []
    files = ['1789-Washington.txt', '1797-Adams.txt', '1801-Jefferson.txt']
    for file in files:
        corpus.append(inaugural.raw(file))
    corpus.append("how now brown cow")

    for file in corpus:
        tf1 = tf(q[0], file)
        tf2 = tf(q[1], file)
        print "tf: %s is %f" % (q[0], tf1)
        print "tf: %s is %f" % (q[1], tf2)
    i1 = idf(q[0], corpus)
    i2 = idf(q[1], corpus)
    print "IDF1: %s" % (i1,)
    print "IDF2: %s" % (i2, )