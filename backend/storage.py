import os
from functools import lru_cache

from dotenv import load_dotenv

from backend.data import SESSOES, proximo_id_sessao

load_dotenv(".env.local")
load_dotenv()

TABELA_SESSOES = "sessoes_estudo"


@lru_cache(maxsize=1)
def cliente_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None

    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(url, key)


def listar_sessoes():
    cliente = cliente_supabase()
    if cliente is None:
        return SESSOES

    try:
        resposta = cliente.table(TABELA_SESSOES).select("*").order("id", desc=False).execute()
    except Exception:
        return SESSOES

    return resposta.data or SESSOES


def registrar_sessao(sessao: dict) -> dict:
    sessao = dict(sessao)
    cliente = cliente_supabase()
    if cliente is None:
        sessao["id"] = proximo_id_sessao()
        SESSOES.append(sessao)
        return sessao

    try:
        resposta = cliente.table(TABELA_SESSOES).insert(sessao).execute()
    except Exception:
        sessao["id"] = proximo_id_sessao()
        SESSOES.append(sessao)
        return sessao

    if resposta.data:
        return resposta.data[0]
    return sessao
