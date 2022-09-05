from pymongo import MongoClient
import pymongo
import os

CONN_STR = os.environ["GH_CONN_STR"]

def get_database(dbname):
    client = MongoClient(CONN_STR)
    return client[dbname]