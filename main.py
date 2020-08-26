from __future__ import unicode_literals
import os
from flask import Flask, request
import tweepy
import twint
import re
import service
import keras
from twilio.rest import Client
from twilio import twiml
from textgenrnn import textgenrnn
from datetime import datetime

app = Flask(__name__)

# authentication for Twilio
client = Client(os.environ.get('PHONE_KEY'), os.environ.get('PHONE_SECRET'))

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
    service.getTweetsHelper(user)
    return "Tweets saved on " + user + ".txt"

@app.route("/generate")
def generate():
    startTime = datetime.now()
    textgen = textgenrnn()
    textgen.train_from_file('marchahmadness.txt', new_model=True, num_epochs=300, gen_epochs=50, word_level=True)
    textgen.generate()
    print(datetime.now() - startTime)
    return "Generated tweets"

@app.route("/generateFromTrained")
def generateFromTrained():
    textgen_2 = textgenrnn(weights_path='ahmad_textgenrnn_weights.hdf5',
                       vocab_path='ahmad_textgenrnn_vocab.json',
                       config_path='ahmad_textgenrnn_config.json')
    textgen_2.generate(10, temperature=1.0)
    return "Returned"

@app.route("/sendText")
def sendText():
    client.messages.create(to=os.environ.get('MY_NUMBER'), 
                       from_=os.environ.get('TWILIO_NUMBER'), 
                       body="Hello!")
    return "text"

@app.route("/getText", methods=['POST'])
def getText():
    message_body = request.form['BODY']
    resp = twiml.Response()
    resp.message(message_body)
    return str(resp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)