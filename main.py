from __future__ import unicode_literals

import os
from flask import Flask, request
import tweepy
import twint
import logging
import re
import service
import tensorflow as tf
import numpy as np
import os
import time

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
        parsedStr = service.parsingString(i.tweet)
        if parsedStr.strip():
            file1.write(parsedStr + "\n")
    file1.close()
    return "Tweets saved on " + user + ".txt"

@app.route("/generate")
def generate():
    # path_to_file = tf.keras.utils.get_file('eggsand_toast.txt', './eggsand_toast.txt')
    text = open('./eggsand_toast.txt', 'rb').read().decode(encoding='utf-8')
    print ('Length of text: {} characters'.format(len(text)))

    # Grabbing the unique characters in this text
    vocab = sorted(set(text))

    # Mapping every string to a numerical representation
    char2idx = {u:i for i, u in enumerate(vocab)}
    idx2char = np.array(vocab)

    text_as_int = np.array([char2idx[c] for c in text])
    return "hello"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)