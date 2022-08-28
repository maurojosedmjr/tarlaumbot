from platform import architecture
from typing import Dict, Any, Union, List
from telegram import Update
from telegram.ext import ContextTypes
import requests
import logging

logger = logging.getLogger(__name__)

DEFAULT_ENCODE: str = "UTF-8"
URL_FOR_DEVS: str = "https://www.4devs.com.br/ferramentas_online.php"
PARSE_FUNCTION_CALL_4DEVS: Dict[str, Dict[str, Union[List[str], str]]] = {
    "RG": {"function": "gerar_rg", "params": ["pontuacao"]},
    "CPF": {"function": "gerar_cpf", "params": ["pontuacao", "cpf_estado"]},
    "PIS": {"function": "gerar_pis", "params": ["pontuacao"]},
    "CNPJ": {"function": "gerar_cnpj", "params": ["pontuacao"]},
    "CNH": {"function": "gerar_cnh", "params": []},
    "RENAVAM": {"function": "gerar_renavam", "params": []},
    "CARTAOCRED": {"function": "gerar_cc", "params": ["pontuacao", "bandeira"]},
    "SENHA": {
        "function": "gerar_senha",
        "params": [
            "txt_tamanho",
            "txt_quantidade",
            "ckb_maiusculas",
            "ckb_minusculas",
            "ckb_numeros",
            "ckb_especiais",
        ],
    },
}
FUNCOES: str = ", ".join(
    [function_name for function_name in PARSE_FUNCTION_CALL_4DEVS.keys()]
)


async def get_fordevs(action: str, **kwargs) -> str:
    if "help" in action:
        return f"""
            Uso:
                /4devs FunçãoDesejada ListaDeParametrosExtra
            Exemplo:
                /4devs cpf pontuacao:N
            
            Lista de funções desejadas -> {FUNCOES}
        """
    action_parsed: Dict[
        str, Union[Dict[str, List[str]], str]
    ] = PARSE_FUNCTION_CALL_4DEVS.get(action.upper())

    if not action_parsed:
        return f"Houve um problema. Lista de funções válidas: {FUNCOES}"

    params: Dict[str, Any] = {"acao": action_parsed["function"]}

    if kwargs:
        for k in kwargs.keys():
            if k in action_parsed["params"]:
                params = {**params, **kwargs}

    logger.info(f"CMD: {str(params)}")

    result: requests.Response = requests.post(URL_FOR_DEVS, data=params)
    if result.status_code != 200:
        return "Houve um problema de comunicação com o servidor do 4Devs."
    return result.content.decode("utf-8")


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
