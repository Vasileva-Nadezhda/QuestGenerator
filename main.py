from sqlite3 import Date

import database, models, mongoengine
from dotenv import dotenv_values

config = dotenv_values(".env")

if __name__ == '__main__':
    client = database.startup_db_client()
    mongoengine.connect(db=config["DB_NAME"], host=config["ATLAS_URI"])
    q1=models.Quest("A001", "A", "B", "C", Date(2023, 10, 10), "D", 10, 3)
    q1.save()
    db = client[config["DB_NAME"]]
    quests = db['Quests']
    for i in quests.find():
        print(i)
    database.shutdown_db_client(client)