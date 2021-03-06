"""
Testing code
"""

# Imports
import plac
import logging
import sys
from datetime import datetime
import pandas as pd
import pickle

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.sentiment import SentimentAnalyzer
from gensim import models
from camel_tools.ner import NERecognizer


from SCC.scrapers.facebook import get_fb_posts
from SCC.scrapers.scrape_save import scrape_save_to_cloud, obtain_from_cloud, obtain_kw_from_cloud

from SCC.scrapers.facebook import get_fb_profile
from SCC.utils.DataBase import retrieve_documents
from SCC.utils.cleaning import clean, extract_business_orgs
from SCC.models.TopicModeling import model_from_text

# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')

# constants
GROUP_ID = '130922830337'
N_PAGES = 2  # FB  gropu pages to scrape
N_TOPICS = 4  # Topics for LDA topic model
N_PASSES = 50  # Passes for LDA topic model
model_suffix = '{:%Y-%m-%d}'.format(datetime.now())
filename = "LDA_{}_{}_{}".format(N_TOPICS, N_PASSES, model_suffix)
WEB_DRIVER_PATH = "C:\\Users\\Aly\\chromedriver.exe"
MONGO_CLIENT = "mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority"




def main():
    try:

        scrape_save_to_cloud(MONGO_CLIENT, 'posts_database', 'shophere', GROUP_ID, N_PAGES)

        # topic modelling, LDA
        corpus, id2word = model_from_text(df.clean_text)
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=N_TOPICS, passes=N_PASSES)

        df['topic'] = lda[corpus]
        df['topic_likelihood'] = df['topic'].apply(lambda x: max([b for (a, b) in x]))
        df['topic'] = df['topic'].apply(lambda x: max((probability, topic) for topic, probability in x)[1])
        pickle.dump(lda, open(filename, 'wb'))

    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)
