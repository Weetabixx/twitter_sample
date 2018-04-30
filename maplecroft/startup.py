# -*- coding: utf-8 -*-

try:
         import json
except ImportError:
        import simplejson as json
        
import tweepy

import time
import os
import threading
import requests.packages.urllib3
import requests


from django.db import transaction
from threading import Thread
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from twitter import Twitter
from twitter import OAuth
from twitter import TwitterHTTPError
from twitter import TwitterStream
from sets import Set


# Variables that contains the user credentials to access Twitter API  # Need to be more secretive about this
ACCESS_TOKEN = '4340760208-vqpWpqskrir7NGnBdWJwK9m2NZ81ytMccC0xyfU'
ACCESS_SECRET = 'dZlFUDqkOLeRRW8Ko6WEimwePlt7RbZTvsCkicDciV5vr'
CONSUMER_KEY = 'cR3vCq46nQG8oIWCBDRUJbJy9'  # make this more secret
CONSUMER_SECRET = 'xnFOZObxmhni691kC1yUOUjvppFifpoYZNbOxWIMPFohXj1OFq' # and this also




# listener Class Override
class listener(tweepy.StreamListener):
    
    def on_data(self, data):    
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        
        #print decoded
        print("found one")  # need to add new tweet to our data
        print(decoded)
        return True
        
    def on_error(self, status): # something went wrong
        print status
        if status == 420:
            return False


def stream_api():
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    
    l = listener()
    stream = tweepy.Stream(auth = api.auth, listener=l)
    #only 1 stream per authentication, else 420 error
    try:
        stream.filter(follow = "31726915") # @MaplecroftRisk id
    except:
        print "well this did not work"


#get handle objects
def search_api(handle="@MaplecroftRisk"):
    #establishing connection to twitter REST API
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter = Twitter(auth=oauth)
    #try except, because if account table is empty, we don't search
    try:
        
        #get twitter results using handle objects
        # Search queries to be parsed by Twitter API
        found_posts = twitter.search.tweets(q=handle, result_type='recent', 
                                           lang='en', count=50)
    except:
        pass
    for n in range(len(found_posts['statuses'])): # iterate over all found tweets
        tweetid = found_posts['statuses'][n]['id']
        idList.add(tweetid)
    f = open("mapletweets", "w")
    for num in idList:
        f.write(num)
    f.close()

#launch separate threads fro search and stream
search_thread = Thread(target=search_api)
stream_thread = Thread(target=stream_api)
idList = Set([])
search_thread.start()
stream_thread.start()