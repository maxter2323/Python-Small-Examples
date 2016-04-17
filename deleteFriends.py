import datetime
import time
import tweepy

consumer_key = 'YOU CONSUMER KEY'
consumer_secret = 'YOUR CONSUEMR SECRET'

access_token = 'YOUR ACCESS TOKEN'
access_token_secret = 'YOUR ACCES TOKEN SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
user = api.me()

def recursiveUnfollowing():
    try:
        friends = user.friends()
    except:
        print ("Probably a rate limit exception. I will wait for 15 minutes to continue")
        time.sleep(60 * 15)
        recursiveUnfollowing()
        return
    count = str(len(friends))
    print("COUNT " + count)
    if count == 0:
        print ("Complete")
        return
    for friend in friends:
        print("Unfollowing ", friend.name)
        friend.unfollow()
    recursiveUnfollowing()

print ("Hello " + user.screen_name)
answer = input("Are you sure you want to clear all you friends on twitter?")

if answer == "y":
    recursiveUnfollowing()

print("Finished")
print("Press any key to exit")