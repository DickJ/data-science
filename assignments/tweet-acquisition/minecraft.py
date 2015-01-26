__author__ = 'Rich Johnson'

import tweepy
import urllib

if __name__ == '__main__':
    query = '#microsoft OR #mojang' # user 'nirg' post @ https://github.com/tweepy/tweepy/issues/197
    start = '2015-01-19'
    end = '2015-01-26'

    consumer_key = "7fVQ3PzxbO1BvJDVVnVTA";
    consumer_secret = "I7t4mD9Wm8Otn17XDyj7OPjYnpDxSfJJ5zaKqGOok";
    access_token = "33349294-H5XiEy4CV5ug9htfvkJlaeUAImeYtMbOduiYWxkwF";
    access_token_secret = "d5VEsIiZzs2qoJCloqsHC0asb6mNNpXON1KAlM7vEis";

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    q = urllib.quote_plus(query)  # quote_plus removes special characters and replaces with %xx

    for tweet in tweepy.Cursor(api.search, q=q, since=start, until=end).items(
            200):
        # FYI: JSON is in tweet._json
        print(tweet._json)

    print("\n\n\nDONE!!!\n")