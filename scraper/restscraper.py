#! /usr/bin/env python

import tweepy

consumer_key = raw_input('Consumer Key:')
consumer_secret = raw_input('Consumer Secret:')
access_key = raw_input('Access Key:')
access_secret = raw_input('Access Secret:')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
query = "#yolo"
results = []
#p = 0
#while p<3:
#    print p
#    results.append(api.search(q=query , lang="en", count = 100))
#    p += 1
for p in range(2):
    results.append(r for r in tweepy.Cursor(api.search, q=query, lang="en", count=100, page = p).items())
print ""
print dir(results[0])
for result in results:
    for textresult in result:
        print textresult.text
