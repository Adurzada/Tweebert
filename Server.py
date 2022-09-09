#!/usr/bin/env python
# coding: utf-8

# # EUDEKLI


# In[1]:


# creds to https://huggingface.co/ElKulako/cryptobert
from transformers import TextClassificationPipeline, TFAutoModelForSequenceClassification, AutoTokenizer
model_name = "ElKulako/cryptobert"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name, num_labels = 3,from_pt=True)
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding = 'max_length')
# post_1 & post_3 = bullish, post_2 = bearish
post_1 = " see y'all tomorrow and can't wait to see ada in the morning, i wonder what price it is going to be at. 😎🐂🤠💯😴, bitcoin is looking good go for it and flash by that 45k. "
post_2 = "  alright racers, it’s a race to the bottom! good luck today and remember there are no losers (minus those who invested in currency nobody really uses) take your marks... are you ready? go!!" 
post_3 = " i'm never selling. the whole market can bottom out. i'll continue to hold this dumpster fire until the day i die if i need to." 
df_posts = [post_1, post_2, post_3]
preds = pipe(df_posts)
print(preds)


# # TWITTER 

# In[2]:


# IMPORTS
#!pip install torch
# NEED TENSORFLOW!
import torch
import tweepy
from textblob import TextBlob as tb
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from datetime import datetime
plt.style.use('fivethirtyeight')
# Account
apikey = 'Your Apis'
apisec = 'Your Apis'
# API of this account
accesskey = 'Your Apis'
accesssecret = 'Your Apis'
auth = tweepy.OAuthHandler(apikey,apisec)
auth.set_access_token(accesskey,accesssecret)
api = tweepy.API(auth, wait_on_rate_limit=True)



def getsentiment(query):
    username_tweets = tweepy.Cursor(api.search_tweets, q=(str(query) + " -Giveaway -giveaway -'for free' -filter:retweets lang:en"), result_type='popular', tweet_mode='extended')   
    tweets = [i for i in username_tweets.items(50)]
    info = []
    for tweet in tweets:
        text = tweet._json["full_text"]
        fav = (tweet.favorite_count)
        retw = (tweet.retweet_count)
        date = (tweet.created_at).strftime('%Y/%m/%d')
        author = tweet.author
        info.append([date,author,text,fav,retw])
    df = pd.DataFrame(data = info, columns=['date','a','t','l','r'], index = range(len(info)))
    def clean(t):
        t = re.sub('#[B|b]','b',t)
        #t = re.sub('#[A-Za-z0-9]+','',t)     #remove #s
        t = re.sub('\\n',' ',t) # remove new lines (Enters)
        t = re.sub('https?:\/\/\S+','',t) #removes any hyperlinks
        return t
    df['ct'] = df['t'].apply(clean)
    df.drop(columns=['t'],inplace=True)
    df['sentiment'] = df['ct'].apply(pipe)
    values = algorithm(df)
    
    def visual(values):
        s = 'Bullish: ' + str(values['Bullish']) + '<br>Neutral: ' + str(values['Neutral']) + '<br>Bearish: ' + str(values['Bearish'])
        return s
        
    
    s = visual(values)
    return s
    #get their sentiments
    #calculate the global sentiment 


# # ALGORITHM

# In[3]:


def algorithm(df):
    def esquare(dfelement):
        return np.sqrt(np.sqrt(np.sqrt(dfelement)))
    df['sum'] = df['l'] + df['r']
    df['weight'] = df['sum'].apply(esquare)
    def getscore(x):
        score = x[0]['score']
        return score
    df['score'] = df['sentiment'].apply(getscore)
    values={'Bullish':0,'Bearish':0,'Neutral':0}
    for i in range(len(df.index)):
        row = df.iloc[i]
        values[row.sentiment[0]['label']] += (row.score)**3 * row.weight
    sumvalues = sum(values.values())
    for i in values:
        values[i] = round(values[i] / sumvalues,4) * 100.0
    return values


# # SERVER

# In[4]:


from flask import Flask, request, jsonify
from flask_cors import CORS
#Set up Flaskstrong>:
app = Flask(__name__)
#Set up Flask to bypass CORSstrong>:
cors = CORS(app)
#Create the receiver API POST endpoint:
@app.route("/receiver", methods=["POST"])
def postME():
    #print(request.get_data())
    data = request.get_json()
    d = data
    print(data)
    data = d.split('?:?:?')
    query = data[1]
    mail = data[0]
    sentiment = getsentiment(query)
    print('returning ' + sentiment)

    sentiment = jsonify(sentiment)
    return sentiment


# In[ ]:


app.run(debug=True, use_reloader=False)


# In[ ]:




