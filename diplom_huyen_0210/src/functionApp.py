#scraper, filter, savedata
# Libraries using
import sys
import os
import ntpath
import matplotlib.pyplot as plt
import pandas as pd
import string
import tweepy
import csv
def scrape_tweets(data):
    API_KEY = "vuuHtQehJVLkfQEL7pUxOX4yW"
    API_SECRET = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
    auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    if (not api):
        self.statusBar().showMessage("Can't Authenticate")
        # print ("Can't Authenticate")
        sys.exit(-1)
    searchQuery = '#'+hashtag_input+' since:'+start_day+' until:'+end_day  # this is what we're searching for google since:2016-10-10 until:2016-10-11
    maxTweets = 10000000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    fName = hashtag_input+start_day[5:]+'_'+ end_day[5:]+'.csv' # We'll store the tweets in a text file.


    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1
    tweetCount = 0
    self.statusBar().showMessage("Downloading max {0} tweets".format(maxTweets))
    # print("Downloading max {0} tweets".format(maxTweets))
    with open(fName,'w',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        while tweetCount < maxTweets:
            try:
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
                    self.statusBar().showMessage("No more tweets found")
                    # print("No more tweets found")
                    break
                for tweet in new_tweets:
                    writer.writerow([tweet.id, tweet.created_at, tweet.text])
                    # raw_data.append(json.loads(json.dumps(tweet._json)))
                tweetCount += len(new_tweets)
                self.statusBar().showMessage("Downloaded {0} tweets".format(tweetCount))
                # print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                self.statusBar().showMessage("some error : " + str(e))
                # print("some error : " + str(e))
                break

    # df_tweets = pd.read_csv(fName)
    # df_tweets = df_tweets.fillna('')
    # # replace missing values with '' as in the previous lesson
    # series_count = df_tweets['created_at'].value_counts()
    # # bi xao tron vi tri
    # df_filter = pd.DataFrame()
    # # df_filter["Time"] = series_count.index
    # df_filter['Count'] = [value for value in series_count]
    # df_filter['DateTime'] = pd.to_datetime(df_tweets['created_at'])
    # df_filter.index = df_filter['DateTime']
    # # data_out= df_filter.resample('10Min', label='right').sum().pad()
    # ts = df_filter['Count']
    # df_grouped = ts.resample('10Min').sum()
    # df_grouped = df_grouped.fillna(0)
    # # print(data_out)
    #
    # # df_filter.index = pd.DatetimeIndex(df_filter['Time'])
    # # df_filter = df_filter.resample('10T').mean
    #
    # # print('\n Data Types:', df_filter.dtypes)
    #
    # moving_avg = df_grouped.rolling(window=10).mean()