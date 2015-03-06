__author__ = 'rich'
import nltk
from nltk.corpus import inaugural, stopwords

train = inaugural.raw("1789-Washington.txt")
words = train.split()
words_clean = []
for word in words:
    if word not in stopwords.words("english"):
        words_clean.append(word)

index = {}
for word in words_clean:
    if word in train:
        if word not in index.keys():
            index[word] = ['1789-Washington.txt']
        elif "1789-Washington.txt" not in index[word]:
            index[word].append("1789-Washington.txt")


print "break"