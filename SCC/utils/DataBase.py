import pandas as pd
from pandas import DataFrame


def retrieve_documents(database, collection):

  """ Take a MongoDB database and collection name, and returns all documents in collection to a pandas dataframe"""

  retrieved_documents = database[collection].find()  # do not use database.collection, it is a string :)
  retrieved_df: DataFrame = pd.DataFrame(retrieved_documents)
  return retrieved_df
