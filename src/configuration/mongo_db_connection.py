import os

import sys
import pymongo
import certifi

from src.exception import MyException

from src.logger import logging 
from src.constants import DATABASE_NAME,MONGODB_URL_KEY 
#load the certificate to avoid timeout errors when connecting to MongoDB Atlas
ca = certifi.where()

class MongoDBClient:
    client=None
    
    """ Responsible for creating a MongoDB client and providing access to the database.     """
    def __init__(self, database_name: str = DATABASE_NAME):
        try:
            
            if MongoDBClient.client is None:
                mongo_db_url=os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception (f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
                
            self.client = MongoDBClient.client
            self.database = self.client[DATABASE_NAME]
            self.database_name = database_name
            logging.info(f"MongoDB client created for database: {self.database_name}")
        except Exception as e:
            logging.error(f"Error initializing MongoDB client: {e}")
            raise MyException(e, sys) from e
        
    