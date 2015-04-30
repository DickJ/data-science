__author__ = 'rich'

import datetime
import os
import pandas as pd
from whoosh.fields import Schema
from whoosh.fields import TEXT, ID, DATETIME, KEYWORD
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.query import Term, And, Or
from whoosh.qparser import QueryParser

my_schema = Schema(id = ID(unique=True, stored=True),
                    lang = TEXT(),
                    screenname = TEXT(),
                    tweettext = TEXT(),
                    hashtags = TEXT(),
                    datetime = DATETIME()
                    )

if not os.path.exists("tweets_index"):
    os.mkdir("tweets_index")
    index = create_in("tweets_index", my_schema)
index = open_dir("tweets_index")
writer = index.writer()

df = pd.read_csv('tweets/tweets.csv', header=None, names=['id', 'language', 'screenname', 'tweettext', 'hashtags', 'timestamp'])
for row in df.iterrows():
    try: dt = datetime.datetime.fromtimestamp(int(row[1].timestamp.rstrip("L")))
    except: dt = None
    try: tt = unicode(row[1].tweettext, errors="ignore")
    except: tt = None
    try: ht = unicode((row[1].hashtags).lstrip("[ ").rstrip(" ]"))
    except: ht = None
    try: sn = unicode(row[1].screenname)
    except: sn = None
    writer.add_document(
        id=unicode(row[1].id),
        screenname=sn,
        tweettext=tt,
        hashtags=ht,
        datetime=dt
    )

writer.commit()
