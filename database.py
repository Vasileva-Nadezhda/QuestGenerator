import datetime

from dotenv import dotenv_values
from pymongo import MongoClient
from random import randint
from math import ceil

import models
import mongoengine
import json


def startup_db_client():
    config = dotenv_values(".env")
    mongodb_client = MongoClient(config["ATLAS_URI"])
    mongoengine.connect(db=config["DB_NAME"], host=config["ATLAS_URI"])
    print("Connected to the MongoDB database!")
    return mongodb_client


def shutdown_db_client(mongodb_client):
    mongoengine.disconnect_all()
    mongodb_client.close()


def update_quests():
    d_quests = 0
    w_quests = 0
    quests = models.Quest.objects
    for q in quests:
        if q.deadline < datetime.datetime.now():
            if q.quest_type == 'weekly':
                w_quests += 1
            elif q.quest_type == 'daily':
                d_quests += 1
            q.delete()
    for q in generate_quests(models.User.objects[0], 'weekly', w_quests):
        q.save()
    for q in generate_quests(models.User.objects[0], 'daily', d_quests):
        q.save()


def generate_quests(user: models.User, quest_type, number):
    quests = []
    if quest_type == 'weekly':
        quests_descriptions = json.load(open("weekly_quest_list.json"))
        for i in range(number):
            if user.games_per_day == 0:
                reward = randint(500, 1000)
            elif user.games_per_day == user.wins_per_day:
                reward = randint(10, 100)
            else:
                reward_ratio = (user.games_per_day - user.wins_per_day) / user.games_per_day
                reward = randint(ceil(500 * reward_ratio), ceil(1000 * reward_ratio))
            number_of_quest = randint(0, len(quests_descriptions)-1)
            if user.wins_per_day == 0:
                steps = randint(3, 5)
            elif user.games_per_day == user.wins_per_day:
                steps = randint(10, 15)
            else:
                steps_ratio = user.wins_per_day / user.games_per_day
                steps = randint(ceil(5 * steps_ratio), ceil(10 * steps_ratio))
            date = datetime.datetime.now() + datetime.timedelta(weeks=1)
            quests.append(models.Quest(quests_descriptions[number_of_quest]["title"],
                                       quests_descriptions[number_of_quest]["description"],
                                       reward, date,
                                       "weekly", steps, 0))
    elif quest_type == 'daily':
        quests_descriptions = json.load(open("daily_quest_list.json"))
        for i in range(number):
            if user.games_per_day == 0:
                reward = randint(100, 300)
            elif user.games_per_day == user.wins_per_day:
                reward = randint(10, 30)
            else:
                reward_ratio = (user.games_per_day - user.wins_per_day) / user.games_per_day
                reward = randint(ceil(100 * reward_ratio), ceil(300 * reward_ratio))
            number_of_quest = randint(0, len(quests_descriptions) - 1)
            if user.wins_per_day == 0:
                steps = randint(1, 3)
            elif user.games_per_day == user.wins_per_day:
                steps = randint(5, 10)
            else:
                steps_ratio = user.wins_per_day / user.games_per_day
                steps = randint(ceil(3 * steps_ratio), ceil(5 * steps_ratio))
            date = datetime.datetime.now() + datetime.timedelta(days=1)
            quests.append(models.Quest(quests_descriptions[number_of_quest]["title"],
                                       quests_descriptions[number_of_quest]["description"],
                                       reward, date, "daily",
                                       steps, 0))
    return quests


def update_user():
    user = models.User.objects.first()
    user.games_per_day = randint(0, 10)
    user.wins_per_day = randint(0, user.games_per_day)
    user.save()


def update_progress():
    for quest in models.Quest.objects():
        quest.current_step = randint(0, quest.number_of_steps)
        quest.save()
