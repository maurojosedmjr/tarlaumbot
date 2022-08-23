import os
from re import I
import requests
from dotenv import load_dotenv
from typing import Dict, List, Any
from telegram.ext import ApplicationBuilder, CommandHandler, Updater
from bot import commands
from time import sleep

load_dotenv()

TOKEN: str = os.environ.get("TOKEN")
BASE_URL: str = os.environ.get("BASE_URL")


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler(["start", "help", "ajuda"], commands.start))
    app.add_handler(CommandHandler("teste", commands.motivacional))

    # app.run_polling()
    app.run_webhook(
        listen="0.0.0.0",
        port="443",
        url_path=TOKEN,
        webhook_url=f"{BASE_URL}{TOKEN}/setWebhook",
    )
    # app.run_polling()


def delete_message_channel(message_dict: Dict[str, Any]) -> None:
    chat_id: int = message_dict["message"]["chat"]["id"]
    message_id: int = message_dict["message"]["message_id"]

    print(f"Deletando a mensagem: {message_id}")
    result: requests.Response = requests.post(
        f"{BASE_URL}{TOKEN}/deleteMessage",
        data=dict(chat_id=chat_id, message_id=message_id),
    )
    if result.status_code == 200:
        print("Mensagem apagada com sucesso")
    else:
        print("Ocorreu um erro ao apagar a mensagem")


def delete_message_update(message_dict: Dict[str, Any]) -> None:
    update_id: int = message_dict["update_id"]

    print(f"Deletando a mensagem do update: {update_id}")
    result: requests.Response = requests.post(
        f"{BASE_URL}{TOKEN}/getUpdates", data=dict(offset=update_id + 1)
    )
    if result.status_code == 200:
        print("Mensagem apagada com sucesso")
    else:
        print("Ocorreu um erro ao apagar a mensagem")


def delete_messages_update(list_result: List[Dict[str, Any]]) -> None:
    for message in list_result:
        delete_message_update(message)


if __name__ == "__main__":
    while True:
        while True:
            result: requests.Response = requests.get(f"{BASE_URL}{TOKEN}/getUpdates")
            print(result.json())

            if result.status_code == 200:
                message: Dict[str, Any] = result.json()["result"]

                delete_messages_update(message)

            sleep(2)
