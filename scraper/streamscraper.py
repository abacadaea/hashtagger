#! /usr/bin/env python

import sys
import tweepy
import cPickle as pickle
import string

consumer_key = raw_input('Consumer Key:')
consumer_secret = raw_input('Consumer Secret:')
access_key = raw_input('Access Key:')
access_secret = raw_input('Access Secret:')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    filecounter = 130
    tweetlist = []
    def on_status(self, status):
            tweet= status.text
            tweettag = []
            if tweet[:2] == "RT":
                tweet = tweet [2:]
            tweet = tweet.split()
            new_tweet = []
            for word in tweet:
                if "@" in word: #word[0] == '@':
                    #print tweet
                    pass
                    #print word
                    #tweet.remove(word)
                    #print tweet
                elif word[0] == '#':
                    #tweet.remove(word)
                    tweettag.append("#" + ''.join(ch for ch in word[1:] if ch not in string.punctuation).lower())
                else:
                    new_tweet.append(''.join(ch for ch in word if ch not in string.punctuation).lower())
            #new_tweet = ' '.join(new_tweet)
            #print new_tweet
            if(len(tweettag) > 0):
                print ' '.join(new_tweet) + " tags: " + ' '.join(tweettag)
                self.tweetlist.append((new_tweet, tweettag))
                #print (tweetlist)
            if(len(self.tweetlist) >= 1000):
                pickle.dump(self.tweetlist, open("tweets" + str(self.filecounter), "wb"))
                self.filecounter += 1
                self.tweetlist = []
                print('Wrote file')

    def on_error(self, status_code):
            print >> sys.stderr, 'Encountered error with status code:', status_code
            return True # Don't kill the stream

    def on_timeout(self):
            print >> sys.stderr, 'Timeout...'
            return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(languages=['en'], track=['a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z'])

