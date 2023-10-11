from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")


def startup_db_client():
    mongodb_client = MongoClient(config["ATLAS_URI"])
    print("Connected to the MongoDB database!")
    return mongodb_client


def shutdown_db_client(mongodb_client):
    mongodb_client.close()
