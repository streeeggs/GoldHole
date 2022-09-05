from pymongo import MongoClient
import pymongo
import configparser
import os

config = configparser.ConfigParser()
path = os.path.abspath(os.path.join(".ini"))
config.read(path)

CONN_STR = config["PROD"]["GH_URI"]

def get_database(dbname):
    client = MongoClient(CONN_STR)
    return client[dbname]