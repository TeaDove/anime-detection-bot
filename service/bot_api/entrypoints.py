import asyncio

import uvloop

import nest_asyncio
from presentation.presentation_bot.app import create_app
from presentation.presentation_bot.lambda_handler import LambdaHandler

nest_asyncio.apply()
uvloop.install()

app = create_app()
handler = LambdaHandler(app, asyncio.get_event_loop()).handle

if __name__ == "__main__":
    app.run_polling()
