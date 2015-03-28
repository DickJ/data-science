# Acquiring and Storing Social Media Data #

##Corrections to assignment 2 based on feedback.
###Issue 1: No resiliency in the code.
Resiliency was addded to get_tweets.py:main_download_tweets_s3() in the form of
a KeyboardInterrupt exception. The exception is caught and allows the program to 
finish downloading the current tweet before terminating the process.

###Issue 2: No filtering of tweets’s text on  usernames (@)
The mapper function in tweet_emr.py now contains an updated regex that filters 
out usernames.

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

  