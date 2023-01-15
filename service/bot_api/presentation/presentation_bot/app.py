import uvloop
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

from shared.base import logger
from shared.constants import constants
from shared.settings import app_settings

uvloop.install()


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


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error({"status": "internal.bot.error"}, exc_info=context.error)


def create_app() -> Application:
    application = (
        ApplicationBuilder().pool_timeout(100).connection_pool_size(50000).token(app_settings.bot_token).build()
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_error_handler(error_handler)

    return application
