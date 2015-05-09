__author__ = 'Rich Johnson <richard.johnson@ischool.berkeley.edu>'

from mrjob.job import MRJob
import pandas as pd
import cStringIO
import re


class CountWords(MRJob):
    def mapper(self, _, line):
        df = pd.read_csv(cStringIO.StringIO(line))
        text = df.columns[3]
        # The key is irrelevant, I just want everything to be sent to 1
        # reducer. I could randomly assign an alphabetical key to each tuple in
        # order to spread the load over multiple reducers and add another step
        # to recombine it all at the end, but this way is fine for now.
        yield "a", (len(text), 1)

    def reducer(self, key, values):
        sum = 0.0
        count = 0
        for value in values:
            sum += value[0]
            count += value[1]
        yield "Average: ", sum/count


if __name__ == '__main__':
    CountWords.run()