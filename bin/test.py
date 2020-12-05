"""
Testing code
"""

# Imports
import plac
import os
import logging
import sys
import pandas as pd
# Import the necessary modules for LDA with gensim
from camel_tools.tokenizers.word import simple_word_tokenize

from gensim import matutils, models
import scipy.sparse

import numpy
import pandas
import pymongo
from pymongo import MongoClient
from SCC.scrapers.facebook import get_fb_posts
from SCC.utils.DataBase import retrieve_documents
from SCC.utils.cleaning import clean_text_1, clean_text_2, nouns_adj, extract_business_orgs

from SCC.models.tokenize import tokenize_post
from camel_tools.sentiment import SentimentAnalyzer

from twitter_scraper import get_tweets
from twitter_scraper import get_trends

# Import helper functions
from sklearn.feature_extraction.text import CountVectorizer
from camel_tools.ner import NERecognizer
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

        posts = get_fb_posts(group='130922830337', pages=2)

        if posts:
            fb_group.insert_many(posts)
        else:
            raise Exception("No posts found.")

        db = client["posts_database"]
        df = retrieve_documents(database=db, collection='shophere')
        print (df.columns)

        # clean the free text field

        clean = lambda x: nouns_adj(clean_text_2(clean_text_1(x)))
        #clean = lambda x:x
        data_clean = pd.DataFrame(df.text.apply(clean))
        data_clean.columns = ['post_text']
        data_clean = data_clean.sort_index()
        print(data_clean.head())

        shorten_list = lambda x:x[:50]
        df['tokenized'] = data_clean['post_text'].apply(simple_word_tokenize)
        df['tokenized'] = df["tokenized"].apply(shorten_list) #NER won't accept too long lists
        ner = NERecognizer.pretrained()
        df['NER'] = df.tokenized.apply(ner.predict_sentence)
        df['labels'] = df.apply(lambda x: extract_business_orgs(x.tokenized, x.NER), axis=1)
        print(df['labels'])



        # Create document term matrix
        """
        cv = CountVectorizer(max_df=.8)
        data_cv = cv.fit_transform(data_clean.post_text)
        data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
        data_dtm.index = data_clean.index
        data = data_dtm #copy to keep data_dtm intact

        tdm = data.transpose()
        sparse_counts = scipy.sparse.csr_matrix(tdm)
        corpus = matutils.Sparse2Corpus(sparse_counts)
        id2word = dict((v, k) for k, v in cv.vocabulary_.items())
        
        #The LDA for topic modeling
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=4, passes=10)
        lda.print_topics()
        
        # print(df[['likes']].head(25))
        # print(df['user_id'].head(25))
        # print(df['text'].head(25))
        # print(df.shape)
        # print(df.columns)
        # print('tokenization:::::')
        # print(tokenize_post(df.iloc[1, 2]))
        
        sa = SentimentAnalyzer.pretrained()
        # sentiments = sa.predict(df['text'].head(0))
        sentiment = sa.predict_sentence(' شركة فودافون هي شركة مصرية  ')
        # print(sentiments)
        print('aly')
        print(sentiment)
        

        #mled = MLEDisambiguator.pretrained()
        #tagger = DefaultTagger(mled, 'pos')

        #print(tagger.tag('ذهبت الى المدرسة الجميلة صباحا '.split()))
        """
    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)
