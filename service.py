import re
import twint
import pyAesCrypt
import pickle
import os
import random
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

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
    fortweet =  numbers[random.randrange(len(numbers))]

    pickle.dump(fortweet, open("fortweet.p", "wb"))
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile("fortweet.p", "thistweet.aes", os.environ.get('ENCRYPT'), bufferSize)
    return fortweet

def checkNumber(number):
    bufferSize = 64 * 1024
    pyAesCrypt.decryptFile("thistweet.aes", "fortweet.p", os.environ.get('ENCRYPT'), bufferSize)
    temp = pickle.load(open("fortweet.p", "rb"))
    return number == temp

def newRandomNumbers():
    numbers = [""]
    pickle.dump(numbers, open("numbers.p", "wb"))
    bufferSize = 64 * 1024
    pyAesCrypt.encryptFile("numbers.p", "data.aes", os.environ.get('ENCRYPT'), bufferSize)

def createTweetsFile(ls):
    tweets = []
    for i in ls:
        tweets.append(i)
    pickle.dump(tweets, open("tweets.p", "wb"))

def train():
    file_name = "everyone.txt"
    train_tokenizer(file_name)
    vocab_file = "aitextgen-vocab.json"
    merges_file = "aitextgen-merges.txt"
    config = GPT2ConfigCPU()
    ai = aitextgen(vocab_file=vocab_file, merges_file=merges_file, config=config)
    data = TokenDataset(file_name, vocab_file=vocab_file, merges_file=merges_file, block_size=64)
    ai.train(data, batch_size=16, num_steps=1000)

def generateFromModel():
    ai = aitextgen(model="./trained_model/pytorch_model.bin", vocab_file="./aitextgen-vocab.json", merges_file="./aitextgen-merges.txt", config="./trained_model/config.json")
    ls = ai.generate(3, return_as_list=True, temperature=1.0)
    temp = []
    for i in ls:
        for j in i.split("\r\n"):
            temp.append(j)
    return temp

def test_train():
    ai = aitextgen(tf_gpt2="124M")
    file_name = "everyone.txt"
    ai.train(file_name,
         line_by_line=False,
         from_cache=False,
         num_steps=5000,
         generate_every=1000,
         save_every=1000,
         learning_rate=1e-4,
         batch_size=1, 
         )