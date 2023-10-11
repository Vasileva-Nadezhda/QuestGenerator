from sqlite3 import Date

from dotenv import dotenv_values

import database
import models
import mongoengine

config = dotenv_values(".env")

if __name__ == '__main__':
    client = database.startup_db_client()
    mongoengine.connect(db=config["DB_NAME"], host=config["ATLAS_URI"])
    db = client[config["DB_NAME"]]
    quests = db['Quests']
    for i in quests.find():
        print(i)
    database.shutdown_db_client(client)