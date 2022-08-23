import os
from re import I
from dotenv import load_dotenv
from typing import Dict, Union
from telegram.ext import ApplicationBuilder, CommandHandler, Updater
from bot import commands

load_dotenv()

TOKEN: str = os.environ.get("TOKEN")
BASE_URL: str = os.environ.get("BASE_URL")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler(["start", "help", "ajuda"], commands.start))
    app.add_handler(CommandHandler("teste", commands.motivacional))

    app.run_polling()


if __name__ == "__main__":
    main()
