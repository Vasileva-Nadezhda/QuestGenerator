import telegram_bot

from dotenv import dotenv_values

import database

config = dotenv_values(".env")

if __name__ == '__main__':
    client = database.startup_db_client()
    db = client[config["DB_NAME"]]
    quests = db['Quests']
    for i in quests.find():
        print(i)
    database.update_quests()
    quests = db['Quests']
    for i in quests.find():
        print(i)
    database.shutdown_db_client(client)
