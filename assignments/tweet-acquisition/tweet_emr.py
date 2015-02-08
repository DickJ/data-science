__author__ = 'rich'
#

import re
import string
import sys

from mrjob.job import MRJob

WORD_RE = re.compile(r"[\w']+")


class TweetJob(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for word in words:
            # Wold word.strip() work fine?
            word = word.strip(string.punctuation)
            #word = word.lstrip(string.punctuation)
            if not re.match("^http", word):
                yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))


if __name__ == "__main__":
    TweetJob.run()

'''
    files = []
    conn = boto.connect_s3()  # Pass AWS_KEY and AWS_SECRET_KEY if necessary
    bucket = conn.get_bucket("rich-johnson-w205-assignment2")
    #key = Key(bucket)
    for key in bucket.get_all_keys():
        files.append(key)
    filenum = 1
    for file in files:
        file.get_contents_to_filename(file.__str__) # TODO Better way to name files
        sys.argv[filenum] = file.__str__

    TweetJob.run()

'''