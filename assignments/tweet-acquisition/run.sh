#!/bin/sh
python get_tweets.py \#microsoft+OR+\#mojang 2015-02-01 2015-02-08
python tweet_emr.py -r emr s3://rich-johnson-w205-assignment2/get-tweets-output/ --no-output --output-dir s3://rich-johnson-w205-assignment2/emr-out/