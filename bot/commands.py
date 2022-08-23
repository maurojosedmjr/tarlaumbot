from typing import Callable
from telegram import Update
from telegram.ext import ContextTypes
import json
import requests
from enum import Enum

DEFAULT_ENCODE: str = "UTF-8"
URL_FOR_DEVS: str = "https://www.4devs.com.br/ferramentas_online.php"

CPFCall: Callable = lambda _: requests.get(
    URL_FOR_DEVS, data={"acao": "gerar_cpf", "pontuacao": "N"}
).content.decode(DEFAULT_ENCODE)


class ParserFunctions4Devs(Enum):
    CPF = CPFCall


def get_fordevs(valor) -> str:
    r_pis = requests.post(URL_FOR_DEVS, data=dict(acao="gerar_pis", pontuacao="N"))
    pis_da_vez = r_pis.content.decode("utf-8")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Pois não meu padrinho."
    )


async def for_dev(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="")
