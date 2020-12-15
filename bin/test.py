"""
Testing code
"""

# Imports
import plac
import logging
import sys
import os
import pickle



from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.sentiment import SentimentAnalyzer
from gensim import models
from gensim.corpora import Dictionary
from camel_tools.ner import NERecognizer

from SCC.scrapers.scrape_save import obtain_from_cloud, obtain_kw_from_cloud

from SCC.utils.cleaning import clean, extract_business_orgs
from SCC.models.TopicModeling import model_from_text

# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')

# constants
WEB_DRIVER_PATH = "C:\\Users\\Aly\\chromedriver.exe"
MODEL_PATH = "C:\\Users\\Aly\\PycharmProjects\\Smart-Contact-Center\\bin\\LDA_4_50_2020-12-14"
MONGO_CLIENT = "mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority"
TELECOM_ = "vodafone we etisalat orange وي فودافون اتصالات اورانج أورانج إتصالات"

@plac.annotations(
    model_path=plac.Annotation(
        'Path where the model is stored.',
        type=str
    ),
    keywords = plac.Annotation(
        'List of strings of the companies to search for in the posts.',
        type=str
    )
)

def main(
        model_path= MODEL_PATH, keywords=TELECOM_
):
    """ Infer for each post, its sentiment, list of named entities, and topics """
    try:
        search_text = ' '.join(keywords)
        df = obtain_kw_from_cloud(TELECOM_, MONGO_CLIENT, 'posts_database', 'shophere')

        df['clean_text'] = df.text.apply(clean)
        df['tokenized'] = df['clean_text'] \
            .apply(simple_word_tokenize) \
            .apply(lambda x: x[:50])  # NER won't accept too long lists

        # Named entity recognizer
        ner = NERecognizer.pretrained()
        df['NER'] = df.tokenized.apply(ner.predict_sentence)
        df['named_entities'] = df.apply(lambda x: extract_business_orgs(x.tokenized, x.NER), axis=1)

        # sentiment analyzer
        sa = SentimentAnalyzer.pretrained()
        df['sentiment'] = df.clean_text.apply(sa.predict_sentence)

        # topic modelling, LDA

        #corpus = df.clean_text.apply(list).apply(Dictionary.doc2bow)
        corpus, id2word = model_from_text(df.clean_text)
        lda = pickle.load(open(model_path, 'rb'))
        df['topic'] = lda[corpus]
        df['topic_likelihood'] = df['topic'].apply(lambda x: max([b for (a, b) in x]))
        df['topic'] = df['topic'].apply(lambda x: max((probability, topic) for topic, probability in x)[1])

        df.to_csv('final.csv', encoding='UTF-8')
        lda.print_topics()
        print(df['topic'])
        print(df['sentiment'])
        print(df['named_entities'])

    except Exception:
        logger.exception('Exception occurred in running test function')


if __name__ == '__main__':
    plac.call(main)
