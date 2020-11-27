import pandas as pd
from facebook_scraper import get_posts
import pymongo
from pymongo import MongoClient

SEARCH_LIMIT = 10
posts = []

for post in get_posts(group='130922830337', pages=2): # group ID for don't shop here group
    posts.append(post)

# connect to client
client = MongoClient("mongodb+srv://aly:a@cluster0.4pfcp.mongodb.net/db?retryWrites=true&w=majority")
#create a database
db = client["posts_database"]
#create a collection (a table)
fb_group = db["shophere"]
db['shophere'].delete_many({})
fb_group.insert_many(posts)


def retrieve_documents(database, collection):
  ''' Take a MongoDB database and collection name, and returns all documents in collection to a pandas dataframe'''
  retrieved_documents = database[collection].find() #do not use database.collection, it is a string :)
  retrieved_df = pd.DataFrame(retrieved_documents)
  return retrieved_df

db = client["posts_database"]
df = retrieve_documents(database = db , collection = 'shophere')

print(df['text'].head())