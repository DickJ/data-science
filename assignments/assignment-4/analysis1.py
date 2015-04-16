__author__ = 'Rich Johnson <richard.johnson@ischool.berkeley.edu>'

from mrjob.job import MRJob
import pandas as pd
import cStringIO
import re


class CountWords(MRJob):
    def mapper(self, _, line):
        df = pd.read_csv(cStringIO.StringIO(line))
        text = df.columns[3].strip()
        # print text
        for word in text.split():
            word = word.lower()
            if not re.match("(^https?://|^pic\.twitter\.com|^@)", word):
                word = re.sub("^#", "", word)
                word = re.sub('[\[\]!"&()*+,./:;<=>?@[\]^_`{|}~]', "", word)
                yield word, 1

    def reducer(self, key, value):
        yield key, sum(value)


if __name__ == '__main__':
    CountWords.run()