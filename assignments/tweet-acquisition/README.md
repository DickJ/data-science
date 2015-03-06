# Acquiring and Storing Social Media Data #


##1. 
Output from get_tweets.py can be found at 
s3://rich-johnson-w205/assignment2/get-tweets-output/ . The files in this bucket
 contain just the text strings of tweets from date specified in the filename
 
Output from tweet_emr can be found at 
s3://rich-johnson-w205-assignment2/emr-out .The files in this bucket is the 
output from running map reduce on the tweets specified above. The file 
contained in this folder holds word frequency counts.

##2. 
My twitter acquisition code can be found in get_tweets.py and tweet_emr.py.

##3. 
My histogram can be found in ./R/WordFreqHist.png and WordFreqLogLog.png
I dumped the data from emr in to R and produced histograms using that. The 
log-log histogram shows an approximate Zipf distribution, but there are some 
problems with the stacking that show some negatives, so I also included a 
x-axis-log histogram.

  