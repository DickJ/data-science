import pymongo

tags = ["#ALG", "#ARG", "#AUS", "#BEL", "#BIH", "#BRA", "#CHI", "#CIV", "#CMR",
        "#COL", "#CRC", "#CRO", "#ECU", "#ENG", "#ESP", "#FRA", "#GER", "#GHA",
        "#GRE", "#HON", "#IRN", "#ITA", "#JPN", "#KOR", "#MEX", "#NED", "#NGA",
        "#POR", "#RUS", "#SUI", "#URU", "#USA"]

conn = pymongo.MongoClient()
db = conn.assignment4
coll = db.tweets

for tag in tags:
    counter = 0
    for doc in coll.find({'hashtags':{'$regex':tag}}):
        counter +=1
    print tag + ":\t" + str(counter)
