#! /usr/bin/env python

import csv
import sys
import string
import cPickle as pickle

csvfile = open(sys.argv[1], 'rb')
reader = csv.reader(csvfile, dialect='excel')

tweetlist = []
for row in reader:
    print row[3]
    tweet = row[3]
    tweettag = []
    if tweet[:2] == "RT" or tweet[:2] == "rt":
        tweet = tweet[2:]
    tweet = tweet.split()
    new_tweet = []
    for word in tweet:
        if "@" in word:
            pass
        elif word[0] == "#":
            tweettag.append("#" + ''.join(ch for ch in word[1:] if ch not in string.punctuation).lower())
        else:
           new_tweet.append(''.join(ch for ch in word if ch not in string.punctuation).lower())
    if(len(tweettag) >0):
        print ' '.join(new_tweet) + " tags: " + ' '.join(tweettag)
        print (new_tweet, tweettag)
        tweetlist.append((new_tweet, tweettag))
pickle.dump(tweetlist, open(sys.argv[1]+".pickle", "wb"))
print "Done. Wrote file."
