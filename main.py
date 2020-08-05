from __future__ import unicode_literals

import os
from flask import Flask, request
import tweepy
import twint
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


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
    tweets = []
    user = request.args.get('user')
    c = twint.Config()
    c.Username = user
    c.Hide_output = True
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    logging.info("Searching tweets for " + user)
    twint.run.Search(c)
    logging.info("Saving tweets to " + user + ".txt file")
    file1 = open(user + ".txt", "w")
    for i in tweets:
        parsedStr = remove_emoji(i.tweet)
        parsedStr = re.sub(r"http\S+", "", parsedStr)
        parsedStr = re.sub(r'pic.twitter.com/[\w]*', "", parsedStr)
        parsedStr = re.sub(r'^https?:\/\/.*[\r\n]*', '', parsedStr, flags=re.MULTILINE)
        parsedStr = re.sub(r'@[\w]*', '', parsedStr)
        parsedStr = re.sub(r'…', '', parsedStr)
        if parsedStr.strip():
            file1.write(parsedStr + "\n")
    file1.close()
    
    return "Tweets saved on " + user + ".txt"

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)