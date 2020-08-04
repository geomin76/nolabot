from __future__ import unicode_literals

import os
from flask import Flask, request
import tweepy
import twint


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
    c = twint.Config()
    c.Username = user
    c.Hide_output = True
    c.Store_csv = True
    c.Output = user + ".csv"
    twint.run.Search(c)
    return "Tweets saved on " + user + ".csv"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)