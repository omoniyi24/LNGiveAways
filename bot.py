import tweepy
import requests
import os

from lnbit import LNbits

class Bot():
    def __init__(self, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET):
        self.CONSUMER_KEY = CONSUMER_KEY
        self.CONSUMER_SECRET = CONSUMER_SECRET
        self.ACCESS_KEY = ACCESS_KEY
        self.ACCESS_SECRET = ACCESS_SECRET

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        self.api = tweepy.API(auth)

    def get_retweets_list(self):
        tweetObj = self.api.get_retweets_of_me()[0].__dict__
        tweetObjJson = tweetObj['_json']
        tweetId = tweetObjJson['id']
        return self.api.get_retweets(tweetId)

    def send_retweeters_dm(self):
        lnbits = LNbits()
        for retweet in self.get_retweets_list():
            print(retweet.user.screen_name)  # printing the screen names of the retweeters
            retweeterId = retweet.user.id  # the ID of the tweeter
            if not retweeterId == 1579128080483991552:
                new_wallet_url = lnbits.get_new_wallet_url()
                direct_message =  self.api.send_direct_message(retweeterId, new_wallet_url)
                print(direct_message)
