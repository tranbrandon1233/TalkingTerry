from dotenv import load_dotenv
import os
from pandas import DataFrame
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = MONGO_DB_URI + 'MyFirstDatabase'
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['Terry']
  

def sendToDB(data):
   # Get the database
    dbname = get_database()
   # Create a new collection
    collection_name = dbname["memories"]
   # Insert the data
    items = collection_name.find()

    df = DataFrame(items)
    print(df)
  
sendToDB("test")
