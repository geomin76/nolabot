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
# sys.path.append('./textgenrnn')
# from textgenrnn import textgenrnn

# pay for actual subscription   

# rebuild model, trying to include everyone? find best way to build model
    # find ahmad's best tweets and build with everyone elses? danya, lexi, sparsh, becca, ahmad
    # build model with everyone and possible non-word level, but we will see

# parser for text coming in

# add security key
# cron job for flow (at end)

app = Flask(__name__)

# authentication for Twilio
client = Client(os.environ.get('PHONE_KEY'), os.environ.get('PHONE_SECRET'))

# authentication for twitter
auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SECRET'))
auth.set_access_token(os.environ.get('TOKEN'), os.environ.get('TOKEN_SECRET'))
api = tweepy.API(auth)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/tweet")
def tweet():
    # api.update_status("Hello, World!")
    return "Tweeted!"

@app.route("/getUserTweets")
def getTweets():
    user = request.args.get('user')
    service.getTweetsHelper(user)
    return "Tweets saved on " + user + ".txt"

@app.route("/train")
def generate():
    startTime = datetime.now()
    service.train()
    print(datetime.now() - startTime)
    return "Generated tweets"

@app.route("/generateFromTrained")
def generateFromTrained():
    service.generateFromModel()
    return "Returned"

@app.route("/sendText")
def sendText():
    number = service.randomNumber()
    client.messages.create(to=os.environ.get('MY_NUMBER'), 
                       from_=os.environ.get('TWILIO_NUMBER'), 
                       body="Welcome to Nolabot!")
    return "text"

@app.route("/sms", methods=['GET', 'POST'])
def sms():
    number = request.form['From']
    message_body = request.form['Body']
    print(str(number))
    print(str(message_body))

    if service.checkNumber(number):
        resp = MessagingResponse()
        resp.message("Thanks for texting nolabot! Check out the new tweet at https://twitter.com/nolathedog1!")
        return str(resp)
    else:
        resp = MessagingResponse()
        resp.message("It's not your turn to tweet this time, sorry!")
        return str(resp)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)