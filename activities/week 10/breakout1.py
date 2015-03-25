import glob
import io
from whoosh.fields import Schema
from whoosh.fields import TEXT, ID
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.query import Term, And, Or
from whoosh.qparser import QueryParser

import os

print os.getcwd()

my_schema = Schema(id = ID(unique=True, stored=True), 
                    path = ID(stored=True), 
                    source = ID(stored=True),
                    author = TEXT(stored=True), 
                    title = TEXT(stored=True),
                    text = TEXT)

if not os.path.exists("gutenberg1"):
    os.mkdir("gutenberg1")
    index = create_in("gutenberg1", my_schema)

index = open_dir("gutenberg1")

"""
writer = index.writer()

for file in glob.glob("gutenberg/*.txt"):
    #print "getting file: %s" % (file,)
    #print file.split('/')
    a = file.split("-")
    myid = unicode(file)
    mypath = unicode(file)
    mysource = unicode(file.split("/")[1])
    myauthor = unicode(a[0])
    mytitle = unicode(a[1])
    try:
        mytext = io.open(file, encoding="utf-8").read()
    except:
        print "%s: fail whale" % (file,)
        mytext = u"This file sucks"
    writer.add_document(id=myid, path= mypath, source= mysource, author=myauthor, title=mytitle, text=mytext)

writer.commit()
"""
searcher = index.searcher()

query = Term("text", "beginning")
results = searcher.search(query)
print(len(results))
print(results[0])

parser = QueryParser("text", index.schema)
p = parser.parse("(Adam AND Eve)")
s = searcher.search(p)
print s[0]