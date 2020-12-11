"""
Testing code
"""

# Imports
import plac
import logging
import sys
from datetime import datetime
import pickle

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.sentiment import SentimentAnalyzer
from gensim import models
from camel_tools.ner import NERecognizer

from pymongo import MongoClient

from SCC.scrapers.facebook import get_fb_posts
from SCC.scrapers.facebook import get_fb_profile
from SCC.utils.DataBase import retrieve_documents
from SCC.utils.cleaning import clean, extract_business_orgs
from SCC.models.TopicModeling import model_from_text

# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')

# constants
N_PAGES = 1  # FB  gropu pages to scrape
N_TOPICS = 4  # Topics for LDA topic model
N_PASSES = 1  # Passes for LDA topic model
model_suffix = '{:%Y-%m-d}'.format(datetime.now())
filename = "LDA_{}_{}_{}".format(N_PAGES, N_TOPICS, N_PASSES)
WEB_DRIVER_PATH = "C:\\Users\\Aly\\chromedriver.exe"


def main():
    try:
        gender = get_fb_profile(WEB_DRIVER_PATH, 'alygrps@yahoo.com', 'Compaq8510', 'https://www.facebook.com/tohiiiiii')
        print(gender)
        """
        client = MongoClient("mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority")

        # create a database
        db = client["posts_database"]

        # create a collection (a table)
        fb_group = db["shophere"]

        # reset the collection
        db['shophere'].delete_many({})

        for n, post in enumerate(get_fb_posts(group='130922830337', pages=1)):
            print(n, post)
            fb_group.insert(post)
        """
        """
        # connect to MongoDB client
        client = MongoClient("mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority")

        # create a database
        db = client["posts_database"]

        # create a collection (a table)
        fb_group = db["shophere"]

        # reset the collection
        db['shophere'].delete_many({})

        posts = get_fb_posts(group='130922830337', pages=N_PAGES)

        if posts:
            fb_group.insert_many(posts)
        else:
            raise Exception("No posts found.")

        # Connect to MongoDB and retrieve documents
        db = client["posts_database"]
        df = retrieve_documents(database=db, collection='shophere')

        df.drop(['post_text', 'shared_text', 'image', 'video', 'video_thumbnail', 'video_id', 'images'], axis=1,
                inplace=True)

        # clean the free text field

        df['clean_text'] = df.text.apply(clean)
        df['tokenized'] = df['clean_text'] \
            .apply(simple_word_tokenize) \
            .apply(lambda x: x[:50])  # NER won't accept too long lists

        ner = NERecognizer.pretrained()
        df['NER'] = df.tokenized.apply(ner.predict_sentence)
        df['named_entities'] = df.apply(lambda x: extract_business_orgs(x.tokenized, x.NER), axis=1)

        sa = SentimentAnalyzer.pretrained()
        df['sentiment'] = df.clean_text.apply(sa.predict_sentence)

        corpus, id2word = model_from_text(df.clean_text)

        # The LDA for topic modeling
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=N_TOPICS, passes=N_PASSES)
        pickle.dump(lda, open(filename, 'wb'))
        #with open('LDA_1_1_1', 'rb') as fn:
        #    lda=pickle.load(fn)

        df['topic'] = lda[corpus]
        df['topic_likelihood'] = df['topic'].apply(lambda x: max([b for (a, b) in x]))
        df['topic'] = df['topic'].apply(lambda x: max((probability, topic) for topic, probability in x)[1])

        lda.print_topics()
        print(df['topic'])
        print(df['sentiment'])
        print(df['named_entities'])

        """

    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)
