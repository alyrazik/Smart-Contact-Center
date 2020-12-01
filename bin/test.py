"""
Testing code
"""

# Imports
import plac
import os
import logging
import sys
import numpy
import pandas
import pymongo
from pymongo import MongoClient
from SCC.scrapers.facebook import get_fb_posts
from SCC.utils.DataBase import retrieve_documents
#from SCC.models.tokenize import tokenize_post
from camel_tools.sentiment import SentimentAnalyzer



# Import helper functions
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from time import time
from datetime import datetime



# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')

def main():
    try:
        # connect to client
        client = MongoClient("mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority")
        # create a database
        db = client["posts_database"]
        # create a collection (a table)
        fb_group = db["shophere"]
        db['shophere'].delete_many({})

        posts = get_fb_posts(group='130922830337', pages=1)

        if posts:
            fb_group.insert_many(posts)
        else:
            raise Exception("No posts found.")

        db = client["posts_database"]
        df = retrieve_documents(database=db, collection='shophere')

        print(df[['likes']].head(25))
        print(df['user_id'].head(25))
        print(df['text'].head(25))
        print(df.shape)
        print(df.columns)
        print('tokenization:::::')
        #print(tokenize_post(df.iloc[1, 2]))

        sa = SentimentAnalyzer.pretrained()
        sentiments = sa.predict(df['text'].head(0))
        sentiment = sa.predict_sentence('ايجابي   ')
        print(sentiments)
        print('aly')
        print(sentiment)

    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)