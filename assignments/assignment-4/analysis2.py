__author__ = 'Rich Johnson <richard.johnson@ischool.berkeley.edu>'

from mrjob.job import MRJob
import pandas as pd
import cStringIO
import re
import time


class CountWords(MRJob):
    def mapper(self, _, line):
        df = pd.read_csv(cStringIO.StringIO(line))
        try:
            date_obj = time.gmtime(int(df.columns[5]))
            date_string = str(date_obj.tm_mon) + '/' + str(date_obj.tm_mday) + ' ' + str(date_obj.tm_hour) + ':00'
            yield date_string, 1
        except ValueError:
            # Should occur on first line, since it is the headers, and on lines
            # where we could not find a timestamp (time=0)
            print "ValueError while converting time."

    def reducer(self, key, value):
        yield key, sum(value)


if __name__ == '__main__':

    CountWords.run()

# time zero = 1402012800