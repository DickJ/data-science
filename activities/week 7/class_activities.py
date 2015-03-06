import csv
import pymongo
import json
#3
records= csv.DictReader(open("activities/week 7/legislators-historic.csv"))

conn = pymongo.Connection()
db = conn['cong_db']
coll = db.mem_db
#4
for record in records:
    coll.insert(record)
#5
coll.count()
#6

for record in coll.find({"gender":"F"}):
    print record

num6 = []
for record in coll.find({"gender":"F", "party": {$ne: "Republican"}}):
    num6.append(record)

num8 = []
for record in coll.find({"$or" :[{"first_name":"John"}, {"first_name":"john"},
          {"first_name":"Joshua"}, {"first_name":"joshua"}]}):
    num8.append(record)

names = {}
for record in coll.find():
    try:
        names[record["first_name"]] += 1
    except:
        names[record["first_name"]] = 1

max = 0
maxname = ""
for name, value in names.items():
    if value > max:
        max = value
        maxname = name

print str(max) + maxname