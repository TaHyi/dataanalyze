#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from twitterscraper import query_tweets
import pandas as pd
import os
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import json
import time
import csv
import io
import tweepy
class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    # access_token = "711603250244493313-xpC5hL1ywjE2eyJyKKyErOv6Zzc1QL8"
# access_token_secret = "R5ibYXz0mSYlp0K2iuQQhytTyFVvQDGWKld0CnmGLRWRb"
# consumer_key = "vuuHtQehJVLkfQEL7pUxOX4yW"
# consumer_secret = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
# MAX_TWEETS = 8000
#
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = API(auth, wait_on_rate_limit=True)
# data = Cursor(api.search, q='mozsprint').items(MAX_TWEETS)
# mozsprint_data = []
#     # You will use this line in production instead of this
#     # current_working_dir = os.path.dirname(os.path.realpath(__file__))
# current_working_dir = "./"
# log_tweets = current_working_dir  + str(time.time()) + '_moztweets.txt'
# with open(log_tweets, 'w') as outfile:
#     for tweet in data:
#         mozsprint_data.append(json.loads(json.dumps(tweet._json)))
#         outfile.write(json.dumps(tweet._json))
#         outfile.write("\n")
# print(mozsprint_data[0])
#
# hashtag= "видео"
# # hashtag_input= "mufc"
# # start_day= "2009-05-10"
# # end_day="2009-05-13"
# starttime= "2017-05-29"
# endtime="2017-05-30"

# def scrapeTweets(self, hashtag, starttime, endtime):


# access_token = "711603250244493313-xpC5hL1ywjE2eyJyKKyErOv6Zzc1QL8"
# access_token_secret = "R5ibYXz0mSYlp0K2iuQQhytTyFVvQDGWKld0CnmGLRWRb"
# consumer_key = "vuuHtQehJVLkfQEL7pUxOX4yW"
# consumer_secret = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
# MAX_TWEETS = 8000
#
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = API(auth, wait_on_rate_limit=True)

data = tweepy.Cursor(api.search, q="#박보검", since="2017-05-29", until="2017-05-30").items(MAX_TWEETS)
import codecs
with codecs.open("aaaaApp.csv", mode='w', encoding='utf-8',errors='replace') as cache:
    # fieldnames = ["id", "created_at", "text"]
    writer = csv.writer(cache)
    writer.writerow(["id", "created_at", "text"])
    for tweet in data:
        writer.writerow([tweet.id_str,tweet.created_at,tweet.text],)
        print(tweet.id_str,tweet.created_at, tweet.text)

# outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in data]

# csvFile = open("result.csv","a")
# csvWriter = csv.writer(csvFile)
# for tweet in tweepy.Cursor(api.search, q="видео", since="2017-05-29", until="2017-05-30").items(MAX_TWEETS):
#     csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
#     print( tweet.created_at, tweet.text)
# csvFile.close()
# data = Cursor(api.search, q="видео", since="2017-05-29", until="2017-05-30").items(MAX_TWEETS)

#     # You will use this line in production instead of this
#     # current_working_dir = os.path.dirname(os.path.realpath(__file__))
# current_working_dir = "./"
# log_tweets = current_working_dir  + str(time.time()) + '_moztweets.txt'
# with open(log_tweets, 'w') as outfile:
#     for tweet in data:
#
#         outfile.write(json.dumps(tweet._json))
#         outfile.write("\n")



# raw_data = {'user': [tweet.user for tweet in data],
#             'id': [tweet.id for tweet in data],
#             'created_at': [tweet.timestamp for tweet in data],
#             'text': [tweet.text for tweet in data]}
# df = pd.DataFrame(raw_data, columns=['user',
#                                      'id',
#                                      'created_at',
#                                      'text'])


# file_name =hashtag + starttime + endtime + '.csv'
#
# header = ["user" , "id", "created_at", "text"]
# path = r"C:\\Users\\TaHyi\\PycharmProjects\\myDiplom\\src\\DataScraped\\"
# df= pd.DataFrame()
# df.to_csv(path+file_name, encoding='utf-16', columns=header)
# with io.open(filename,'r',encoding='utf8') as f:
#     text = f.read()
# process Unicode text

# df.to_csv(file_name + '.csv', encoding='utf-8', columns=header)


# df = pd.read_csv(filenamee,index_col=[] )
# print(df.head())


# data = query_tweets('\'' + '%23' + hashtag_input + '%20since%3A' + start_day + '%20until%3A' + end_day + '\'', )
#
# raw_data = {'user': [tweet.user for tweet in data],
#             'id': [tweet.id for tweet in data],
#             'created_at': [tweet.timestamp for tweet in data],
#             'text': [tweet.text for tweet in data]}
# df = pd.DataFrame(raw_data, columns=['user',
#                                      'id',
#                                      'created_at',
#                                      'text'])
# df.to_csv(hashtag_input + start_day + end_day + '.csv', encoding='utf-8')
# df2 = pd.DataFrame()

# # Open/create a file to append data to
# csvFile = open('result.csv', 'a')
#
# #Use csv writer
# csvWriter = csv.writer(csvFile)
#
# for tweet in tweepy.Cursor(api.search,
#                            q = "google",
#                            since = "2014-02-14",
#                            until = "2014-02-15",
#                            lang = "en").items():
#
#     # Write a row to the CSV file. I use encode UTF-8
#     csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
#     print tweet.created_at, tweet.text
# csvFile.close()