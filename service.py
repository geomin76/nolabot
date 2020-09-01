import re
import twint
import pyAesCrypt
import pickle
import os
import random

def parsingString(string):
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
    parsedStr = emoji_pattern.sub(r'', string)
    parsedStr = re.sub(r"http\S+", "", parsedStr)
    parsedStr = re.sub(r'pic.twitter.com/[\w]*', "", parsedStr)
    parsedStr = re.sub(r'^https?:\/\/.*[\r\n]*', '', parsedStr, flags=re.MULTILINE)
    parsedStr = re.sub(r'@[\w]*', '', parsedStr)
    parsedStr = re.sub(r'…', '', parsedStr)
    return parsedStr

def getTweetsHelper(user):
    tweets = []
    c = twint.Config()
    c.Username = user
    c.Hide_output = True
    c.Store_object = True
    c.Store_object_tweets_list = tweets
    print("Searching tweets for " + user)
    twint.run.Search(c)
    print("Saving tweets to " + user + ".txt file")
    file1 = open(user + ".txt", "w")
    for i in tweets:
        parsedStr = parsingString(i.tweet)
        if parsedStr.strip():
            file1.write(parsedStr + "\n")
    file1.close()

def randomNumber():
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile("data.aes", "numbers.p", os.environ.get('ENCRYPT'), bufferSize)
    numbers = pickle.load(open("numbers.p", "rb"))
    return numbers[random.randrange(len(numbers))]