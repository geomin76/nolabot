from __future__ import unicode_literals

import os
from flask import Flask, request
import tweepy
import twint
import logging
import re
import service
import keras
from twilio.rest import Client
from twilio import twiml
from textgenrnn import textgenrnn
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

client = Client(os.environ.get('PHONE_KEY'), os.environ.get('PHONE_SECRET'))

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
    startTime = datetime.now()
    textgen = textgenrnn()
    textgen.train_from_file('marchahmadness.txt', new_model=True, num_epochs=30, gen_epochs=5, word_level=True)
    textgen.generate()
    print(datetime.now() - startTime)
    return "hello"

@app.route("/generateFromTrained")
def generateFromTrained():
    textgen_2 = textgenrnn('ahmad_textgenrnn_weights.hdf5')
    textgen_2.generate(10, temperature=0.5)
    return "Returned"

@app.route("/sendText")
def sendText():
    client.messages.create(to=os.environ.get('MY_NUMBER'), 
                       from_=os.environ.get('TWILIO_NUMBER'), 
                       body="Hello fucker!")
    return "text"

@app.route("/getText", methods=['POST'])
def getText():
    message_body = request.form['BODY']
    resp = twiml.Response()
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)