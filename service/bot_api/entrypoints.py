from presentation.presentation_bot.app import create_app
from presentation.presentation_bot.lambda_handler import LambdaHandler

app = create_app()


if __name__ == "__main__":
    app.run_polling()
else:
    handler = LambdaHandler(app).handle
