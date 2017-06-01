# -*- coding: utf-8 -*-
import tweepy
import sys
import jsonpickle
import os
import json
import csv
import time
import codecs
API_KEY = "vuuHtQehJVLkfQEL7pUxOX4yW"
API_SECRET = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
searchQuery = '#ОпросОтБатона since:2017-05-26 until:2017-06-01'  # this is what we're searching for google since:2016-10-10 until:2016-10-11
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'ОпросОтБатона25-01.csv' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1
raw_data= []
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with codecs.open(fName, 'w', encoding='utf-16',errors='replace') as f:
    while tweetCount < maxTweets:
        try:
            writer = csv.writer(f)
            writer.writerow(["id", "created_at", "text"])
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                # raw_data.extend([tweet.id_str, tweet.created_at, tweet.text])
                # lst.extend([5, 6, 7])
                raw_data =  {
                            'id': [tweet.id_str],
                            'created_at': [tweet.created_at],
                            'text': [tweet.text]
                            }
                writer.writerow([tweet.id, tweet.created_at, tweet.text] )
                # print(tweet.id_str, tweet.created_at, tweet.text)
                # f.write(json.dumps(tweet._json))
                # f.write("\n")
                # f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                #         '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))

import pandas as pd
from io import StringIO
fName = 'tweetsfixUnitestraw.csv' # We'll store the tweets in a text file.
# df = pd.read_csv(StringIO(fName), sep=' ', keep_default_na=False, na_values=['_'])
df = pd.read_csv(fName, header=0, dtype=object,keep_default_na=False,na_values='', na_filter = False)


# df2.to_csv("dem.csv")
print(df['created_at'].value_counts()[:20])

tweets = pd.DataFrame(raw_data, columns=['id',
                                        'created_at',
                                        'text'])
df = pd.DataFrame(tweets['created_at'].value_counts())
print(df)