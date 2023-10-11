from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import dotenv_values


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Write something to start.")


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
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('res/bhs_logo.png', 'rb'))
    await query.edit_message_text(text=f"The command is executed: {query.data}\nWrite something to continue.")


def run():
    config = dotenv_values(".env")
    application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), answer))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()