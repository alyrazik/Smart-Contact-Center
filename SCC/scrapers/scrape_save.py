import logging
import sys
import pandas as pd
from pymongo import MongoClient
from SCC.scrapers.facebook import get_fb_posts
from SCC.utils.DataBase import retrieve_documents

# setup logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger('Network logger')


def scrape_save_to_cloud(mongo_client, database, table, group_ID, n_pages):
    """
    Scrapes a facebook group and saves the scraped content to a MongoDB

    :param mongo_client: the client name of a cloud MongoDB
    :param database: the name of the database to query
    :param table: the name of the table to query from.
    :param group_ID: the facebook group ID to scrape data from.
    :param n_pages: the number of pages to scrape from the group
    :return: none

    """
    try:

        client = MongoClient(mongo_client)

        # create a database
        db = client[database]
        table = db[table]

        posts_list = get_fb_posts(group=group_ID, pages=n_pages)

        df = pd.DataFrame(posts_list)
        df.to_csv('out.csv', encoding='UTF-8')

        if posts_list:
            table.delete_many({})
            table.insert_many(posts_list)
        else:
            raise Exception("No posts found.")

    except Exception:
        logger.exception('Exception occurred in scraping content from facebook')


def obtain_from_cloud(mongo_client, database, table):
    """
    Obtain data from MongoDB and saves it to a pandas data freme
    :param mongo_client: the client name of a cloud MongoDB
    :param database: the name of the database to query
    :param table: the name of the table to query from.
    :return: returns a dataframe with data.

    """
    try:
        # connect to MongoDB client
        client = MongoClient(mongo_client)
        db = client[database]
        df = retrieve_documents(database=db, collection=table)
        df.drop(['post_text', 'shared_text', 'image', 'video', 'video_thumbnail', 'video_id', 'images'], axis=1,
                inplace=True)

        return df

    except Exception:
        logger.exception('Exception occurred in running test function')
