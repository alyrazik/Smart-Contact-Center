"""
Testing code
"""

# Imports
import plac
import logging
import sys

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.sentiment import SentimentAnalyzer
from gensim import models
from camel_tools.ner import NERecognizer

from pymongo import MongoClient

from SCC.scrapers.facebook import get_fb_posts
from SCC.utils.DataBase import retrieve_documents
from SCC.utils.cleaning import clean, extract_business_orgs
from SCC.models.TopicModeling import model_from_text

# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')


def main():
    try:
        # connect to MongoDB client
        client = MongoClient("mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority")

        # create a database
        db = client["posts_database"]

        # create a collection (a table)
        fb_group = db["shophere"]

        # reset the collection
        db['shophere'].delete_many({})

        posts = get_fb_posts(group='130922830337', pages=1)

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
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=2, passes=1)
        df['topic'] = lda[corpus]
        lda.print_topics()
        print(df['topic'])


    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)
