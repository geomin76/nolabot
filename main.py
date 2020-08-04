from __future__ import unicode_literals

import os
from flask import Flask, request
import tweepy
from twitter_scraper import get_tweets


app = Flask(__name__)

# authentication for twitter
auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SECRET'))
auth.set_access_token(os.environ.get('TOKEN'), os.environ.get('TOKEN_SECRET'))
api = tweepy.API(auth)

@app.route("/")
def main():
    return "Hello, World!"

@app.route("/tweet")
def tweet():
    # api.update_status("Hello, World!")
    return "Tweeted!"

@app.route("/getUserTweets")
def getTweets():
    user = request.args.get('user')
    file1 = open(user + ".txt", "w")
    print("Writing to " + user +".txt")
    for tweet in get_tweets(user, pages=50000):
        if tweet and not tweet['isRetweet'] and not tweet['isPinned']:
            if "https://twitter.com" in tweet['text']:
                arr = tweet['text'].split("https://twitter.com")
                file1.write(arr[0] + "\n")
            elif "pic.twitter.com" in tweet['text']:
                arr = tweet['text'].split("pic.twitter.com")
                file1.write(arr[0] + "\n")
            else:
                file1.write(tweet['text'] + "\n")
    file1.close()
    return "Tweets saved on " + user + ".txt"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)