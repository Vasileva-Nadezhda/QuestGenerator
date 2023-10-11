from mongoengine import *


class Quest(Document):

    quest_id = StringField(required=True)
    title = StringField(max_length=100)
    description = StringField()
    reward = StringField()
    deadline = DateField()
    type = StringField()
    number_of_steps = IntField()
    current_step = IntField()

    meta = {'collection': 'Quests'}

    def __init__(self, quest_id, title, description, reward, deadline, quest_type, number_of_steps, current_step, *args,
                 **values):
        super().__init__(*args, **values)
        self.quest_id = quest_id
        self.title = title
        self.description = description
        self.reward = reward
        self.deadline = deadline
        self.type = quest_type
        self.number_of_steps = number_of_steps
        self.current_step = current_step


class User(Document):

    user_id = IntField()
    wins_per_day = IntField()
    games_per_day = IntField()

    meta = {'collection': 'Users'}

    def __init__(self, user_id, wins_per_day, games_per_day, *args, **values):
        super().__init__(*args, **values)
        self.user_id = user_id
        self.wins_per_day = wins_per_day
        self.games_per_day = games_per_day
