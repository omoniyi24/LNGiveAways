import tweepy
import requests
import json

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

userObj = api.get_retweets_of_me()[0].__dict__['user']
userObjJson = userObj.__dict__['_json']
# retweeterId = userObjJson['id']
retweeterId = 1579796182041522177
text = "This is a Direct Message."

# getting the retweeters
# retweets_list = api.retweet(retweeterId)

# printing the screen names of the retweeters
# for retweet in retweets_list:
#     print(retweet.user.screen_name)

# print(direct_message.message_create['message_data']['text'])
# print(retweeterId)
tweetObj = api.get_retweets_of_me()[0].__dict__
tweetObjJson = tweetObj['_json']
tweetId = tweetObjJson['id']   # the ID of the tweet

ln_withdraw = "https://legend.lnbits.com/withdraw/api/v1/links"

retweets_list = api.get_retweets(tweetId) # getting the retweeters

for retweet in retweets_list:
    print(retweet.user.screen_name) # printing the screen names of the retweeters
    retweeterId = retweet.user.id  # the ID of the tweeter
    if not retweeterId == 1579128080483991552:
        headers = {"Content-Type": "application/json", "X-Api-Key": ""}
        payload = {
            "title": "LN GiveAway",
            "min_withdrawable": 2,
            "max_withdrawable": 3,
            "uses": 1,
            "wait_time": 600000,
            "is_unique": True
        }
        response = requests.post(ln_withdraw, data=payload, headers=headers)
        if(response.status_code == 204):
            print(">>>> ", response.json())
            print(">>>> ", response.__dict__['raw'].__dict__)
            # direct_message =  api.send_direct_message(retweeterId, text, attachment_type="/Users/omoniyiilesanmi/Desktop/Screenshot 2022-10-11 at 10.47.50.png")
        else:
            print("Error Creating Withdrawal")
