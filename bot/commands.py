from typing import Dict, Any
from telegram import Update
from telegram.ext import ContextTypes
import requests

DEFAULT_ENCODE: str = "UTF-8"
URL_FOR_DEVS: str = "https://www.4devs.com.br/ferramentas_online.php"
PARSE_FUNCTION_CALL_4DEVS: Dict[str, str] = {"CPF": "gerar_cpf", "PIS": "gerar_pis"}
FUNCOES: str = ", ".join(
    [function_name for function_name in PARSE_FUNCTION_CALL_4DEVS.keys()]
)


async def get_fordevs(action: str, **kwargs) -> str:
    if "help" in action:
        return f"""
            Uso:
                /4devs FunçãoDejada ListaDeParametrosExtra
            Exemplo:
                /4devs cpf pontuacao:N
            
            Lista de funções desejadas -> {FUNCOES}
        """
    action_parsed: str = PARSE_FUNCTION_CALL_4DEVS.get(action.upper())

    if not action_parsed:
        return f"Houve um problema. Lista de funções válidas: {FUNCOES}"

    params: Dict[str, Any] = {"acao": action_parsed}

    if kwargs:
        params = {**params, **kwargs}

    result: requests.Response = requests.post(URL_FOR_DEVS, data=params)
    if result.status_code != 200:
        return "Houve um problema de comunicação com o servidor do 4Devs."
    return result.content.decode("utf-8")


# async def send_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_document


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Pois não meu padrinho."
    )


async def for_devs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    action: str = args[0]

    kwargs: Dict[str, str] = {}
    for value in args[1:]:
        k, v = value.split(":")
        kwargs.update({k: v})

    result: str = await get_fordevs(action=action, **kwargs)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Comando `{action.upper()}`: {result}"
    )
