from presentation.presentation_bot.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run_polling()
