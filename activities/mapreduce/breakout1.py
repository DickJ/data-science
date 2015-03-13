from mrjob.job import MRJob

class job(MRJob):
    def mapper(self, key, value):
        words = value.split()
        for word in words:
            yield (word, 1)

    def combiner(self, key, values):
        pass

    def reducer(self, key, values):
        pass


if __name__ == '__main__':
    pass
