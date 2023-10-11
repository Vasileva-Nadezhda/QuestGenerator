from mongoengine import *


class Quest(Document):

    title = StringField(max_length=100)
    description = StringField()
    reward = IntField()
    deadline = DateTimeField()
    quest_type = StringField()
    number_of_steps = IntField()
    current_step = IntField()

    meta = {'collection': 'Quests'}

    def __init__(self, title, description, reward, deadline,
                 quest_type, number_of_steps, current_step, *args, **values):
        super().__init__(*args, **values)
        self.title = title
        self.description = description
        self.reward = reward
        self.deadline = deadline
        self.quest_type = quest_type
        self.number_of_steps = number_of_steps
        self.current_step = current_step


class User(Document):

    wins_per_day = IntField()
    games_per_day = IntField()

    meta = {'collection': 'Users'}

    def __init__(self, wins_per_day, games_per_day, *args, **values):
        super().__init__(*args, **values)
        self.wins_per_day = wins_per_day
        self.games_per_day = games_per_day
