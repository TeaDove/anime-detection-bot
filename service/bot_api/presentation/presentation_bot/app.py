from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

from shared.constants import constants
from shared.settings import app_settings


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.resources.start,
        parse_mode="html",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=constants.resources.help,
        parse_mode="html",
    )


def create_app() -> Application:
    application = ApplicationBuilder().token(app_settings.bot_token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    return application
