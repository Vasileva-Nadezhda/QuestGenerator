import threading

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler
from dotenv import dotenv_values

import database
import picture_generator

config = dotenv_values(".env")
client = database.startup_db_client()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Write something to start.")


def update_quests():
    t = threading.Timer(60, update_quests)
    t.daemon = True
    t.start()
    database.update_quests()
    print('Quests were updated.')


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Update User parameters", callback_data="update user")],
        [InlineKeyboardButton("Update quests' progress", callback_data="update progress")],
        [InlineKeyboardButton("Get picture", callback_data="get picture")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'get picture':
        await context.bot.send_photo(chat_id=update.effective_chat.id,
                                     photo=InputFile(picture_generator.create_picture(
                                         client[config["DB_NAME"]]['Quests'].find())))
    elif query.data == 'update user':
        database.update_user()
    elif query.data == 'update progress':
        database.update_progress()
    await query.edit_message_text(text=f"The command is executed: {query.data}\nWrite something to continue.")


def run():
    application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), answer))
    application.add_handler(CallbackQueryHandler(button))
    update_quests()
    application.run_polling()
    database.shutdown_db_client(client)
