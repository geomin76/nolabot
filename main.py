from __future__ import unicode_literals
import os
from flask import Flask, request, render_template
import tweepy
import twint
import re
import service
import keras
from twilio.rest import Client
from twilio import twiml
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
import sys
sys.path.append('./textgenrnn')
from textgenrnn import textgenrnn
from flask_cors import CORS, cross_origin

# do some form of checking for numbers, so no random number will text, database?
    # in a record, do a bunch of random numbers? and then pick one
    # and in another record, store that number every tweet push, so it can only recognize that number? and if another person tries to reply, "sorry not your turn"
# pay for actual subscription   
#random function to text a number for every tweet

# rebuild model, trying to include everyone? find best way to build model
    # find ahmad's best tweets and build with everyone elses? danya, lexi, sparsh, becca, ahmad
    # build model with everyone and possible non-word level, but we will see

# pickle file?????

# random image of nola return too

# add security key
# cron job for flow (at end)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# authentication for Twilio
client = Client(os.environ.get('PHONE_KEY'), os.environ.get('PHONE_SECRET'))

# authentication for twitter
auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SECRET'))
auth.set_access_token(os.environ.get('TOKEN'), os.environ.get('TOKEN_SECRET'))
api = tweepy.API(auth)

@app.route("/")
def main():
    return "Hello World"

@app.route("/tweet")
def tweet():
    # api.update_status("Hello, World!")
    # add a tweet under original tweet, saying "brought to you by nolabot1.herokuapp.com"
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
    # somehow rewrite textgenrnn to print to list and return instead of print to console
    textgen_2 = textgenrnn(weights_path='ahmad_textgenrnn_weights.hdf5',
                       vocab_path='ahmad_textgenrnn_vocab.json',
                       config_path='ahmad_textgenrnn_config.json')
    textgen_2.generate(10, temperature=1.0)
    return "Returned"

@app.route("/sendText")
def sendText():
    client.messages.create(to=os.environ.get('MY_NUMBER'), 
                       from_=os.environ.get('TWILIO_NUMBER'), 
                       body="Welcome to Nolabot!")
    return "text"

@app.route("/sendTextToHMadison")
@cross_origin()
def sendTextToHMadison():
    data = request.get_json()
    msg = """
    From: {0}\n\n
    Message: {1}
    """.format(data["from"], data["msg"])
    client.messages.create(to="+17037729467", 
                       from_=os.environ.get('TWILIO_NUMBER'), 
                       body=msg)
    return "text"

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(str(number))
    print(str(message_body))
    resp = MessagingResponse()
    msg = resp.message("Thanks for texting nolabot! Cheers!")
    msg.media("https://lh3.googleusercontent.com/gq5MtvoDPqkkfW12QmxT8zmP0HuyluaxG_UvPa3A67RYo1j67rukrNjiSMk9s3bYIWxNVW7gNXdGKO6_OhaVCXsnnwBtW5faQjZOohZ4G5MMbDDAA7Ee9WIWRResbTK6Jjfff9b5IUI=w2400")
    print(str(resp))
    return str(resp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)