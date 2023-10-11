import telegram_bot

from dotenv import dotenv_values

config = dotenv_values(".env")

if __name__ == '__main__':
    telegram_bot.run()
