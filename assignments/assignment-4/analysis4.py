__author__ = 'Rich Johnson <richard.johnson@ischool.berkeley.edu>'

from mrjob.job import MRJob
import pandas as pd
import cStringIO
import re

class CountWords(MRJob):
    #def __init__(self):
    tracker = {}

    def mapper(self, _, line):
        df = pd.read_csv(cStringIO.StringIO(line))
        text = df.columns[3].strip()
        words = text.lower().split()
        for word in words:
            for word2 in words:
                # If neither word is a link or a username, and they are not the
                # same word, proceed. Hashtags will be left as-is
                if not re.match("(^https?://|^pic\.twitter\.com|^@)", word) \
                        and not re.match("(^https?://|^pic\.twitter\.com|^@)", word2) \
                        and word is not word2:
                    word = re.sub("^#", "", word)
                    word = re.sub('[\[\]!"&()*+,./:;<=>?@[\]^_`{|}~]' , "", word)
                    yield word, (word2, 1)

    def reducer(self, key, value):
        i = len(self.tracker)
        self.tracker[key] = {}
        for pair in value:
            try:
                self.tracker[key][pair[0]] += 1
            except:
                self.tracker[key][pair[0]] = 1

        for wd in self.tracker[key].keys():
            yield key, (wd, self.tracker[key][wd]) #, key + " occurs " + str(self.tracker[key][wd]) + " time(s) with " + wd)



if __name__ == '__main__':
    CountWords.run()