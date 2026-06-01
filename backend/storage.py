import hashlib
import os
from functools import lru_cache

from dotenv import load_dotenv
from flask import current_app, has_app_context

from backend.data import MATERIAS, SESSOES, proximo_id_materia, proximo_id_sessao

load_dotenv(".env.local")
load_dotenv()

TABELA_SESSOES = "sessoes_estudo"
TABELA_MATERIAS = "materias"
TABELA_USUARIOS = "usuarios_app"
TABELA_PLANOS = "planos_estudo"
USUARIOS_LOCAIS = [
    {
        "id": 1,
        "username": "aluno",
        "senha_hash": hashlib.sha256("1234".encode("utf-8")).hexdigest(),
    }
]


@lru_cache(maxsize=1)
def cliente_supabase():
    if has_app_context() and current_app.config.get("TESTING"):
        return None

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        return None

    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(url, key)


def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def autenticar_usuario(username: str, senha: str) -> bool:
    username = (username or "").strip()
    senha_hash = gerar_hash_senha(senha or "")

    cliente = cliente_supabase()
    if cliente is not None:
        try:
            resposta = (
                cliente.table(TABELA_USUARIOS)
                .select("senha_hash")
                .eq("username", username)
                .limit(1)
                .execute()
            )
            if resposta.data:
                return resposta.data[0].get("senha_hash") == senha_hash
        except Exception:
            pass

    return any(
        usuario["username"] == username and usuario["senha_hash"] == senha_hash
        for usuario in USUARIOS_LOCAIS
    )


def cadastrar_usuario(username: str, senha: str):
    username = (username or "").strip()
    senha = senha or ""

    if len(username) < 3:
        return None, "O usuario precisa ter pelo menos 3 caracteres."
    if len(senha) < 4:
        return None, "A senha precisa ter pelo menos 4 caracteres."

    senha_hash = gerar_hash_senha(senha)
    usuario = {"username": username, "senha_hash": senha_hash}

    cliente = cliente_supabase()
    if cliente is not None:
        try:
            existe = (
                cliente.table(TABELA_USUARIOS)
                .select("id")
                .eq("username", username)
                .limit(1)
                .execute()
            )
            if existe.data:
                return None, "Usuario ja cadastrado."

            resposta = cliente.table(TABELA_USUARIOS).insert(usuario).execute()
            if resposta.data:
                novo = dict(resposta.data[0])
                novo.pop("senha_hash", None)
                return novo, None
        except Exception:
            pass

    if any(item["username"] == username for item in USUARIOS_LOCAIS):
        return None, "Usuario ja cadastrado."

    usuario["id"] = len(USUARIOS_LOCAIS) + 1
    USUARIOS_LOCAIS.append(usuario)
    retorno = dict(usuario)
    retorno.pop("senha_hash", None)
    return retorno, None


def listar_sessoes():
    cliente = cliente_supabase()
    if cliente is None:
        return SESSOES

    try:
        resposta = (
            cliente.table(TABELA_SESSOES)
            .select("*, materias(nome)")
            .order("id", desc=False)
            .execute()
        )
    except Exception:
        return SESSOES

    dados = resposta.data or []
    return [normalizar_sessao(item) for item in dados] or SESSOES


def listar_materias():
    cliente = cliente_supabase()
    materias_base = []
    if cliente is not None:
        try:
            resposta = cliente.table(TABELA_MATERIAS).select("*").order("id", desc=False).execute()
            materias_base = resposta.data or []
        except Exception:
            materias_base = MATERIAS
    else:
        materias_base = MATERIAS

    materias = {
        materia["nome"]: {
            **materia,
            "total_minutos": 0,
            "total_sessoes": 0,
        }
        for materia in materias_base
    }
    for sessao in listar_sessoes():
        nome = sessao.get("materia") or sessao.get("nome")
        if not nome:
            continue
        if nome not in materias:
            materias[nome] = {
                "id": len(materias) + 1,
                "nome": nome,
                "cor": cor_por_nome(nome),
                "prioridade": "baixa",
                "descricao": None,
                "total_minutos": 0,
                "total_sessoes": 0,
            }
        materias[nome]["total_minutos"] += int(sessao.get("duracao_minutos") or 0)
        materias[nome]["total_sessoes"] += 1

    for materia in materias.values():
        if not materia.get("descricao"):
            materia["descricao"] = (
                f"{materia['total_sessoes']} sessao(oes) registrada(s), "
                f"{materia['total_minutos']} minuto(s) estudado(s)."
            )

    return list(materias.values())


def obter_materia(materia_id: int):
    cliente = cliente_supabase()
    if cliente is not None:
        try:
            resposta = cliente.table(TABELA_MATERIAS).select("*").eq("id", materia_id).limit(1).execute()
            if resposta.data:
                return resposta.data[0]
        except Exception:
            pass

    return next((materia for materia in MATERIAS if materia["id"] == materia_id), None)


def criar_materia(dados: dict):
    materia = dict(dados)
    cliente = cliente_supabase()
    if cliente is not None:
        try:
            resposta = cliente.table(TABELA_MATERIAS).insert(materia).execute()
            if resposta.data:
                return resposta.data[0]
        except Exception:
            pass

    materia["id"] = proximo_id_materia()
    MATERIAS.append(materia)
    return materia


def atualizar_materia(materia_id: int, dados: dict):
    cliente = cliente_supabase()
    if cliente is not None:
        try:
            resposta = (
                cliente.table(TABELA_MATERIAS)
                .update(dict(dados))
                .eq("id", materia_id)
                .execute()
            )
            if resposta.data:
                return resposta.data[0]
        except Exception:
            pass

    materia = obter_materia(materia_id)
    if materia is None:
        return None
    materia.update(dados)
    materia["id"] = materia_id
    return materia


def excluir_materia(materia_id: int):
    cliente = cliente_supabase()
    materia = obter_materia(materia_id)
    if materia is None:
        materia = next(
            (item for item in listar_materias() if int(item.get("id", 0)) == int(materia_id)),
            None,
        )
        if materia is None:
            return None

    if cliente is not None:
        try:
            cliente.table(TABELA_PLANOS).delete().eq("materia_id", materia_id).execute()
            cliente.table(TABELA_SESSOES).delete().eq("materia_id", materia_id).execute()
            resposta = cliente.table(TABELA_MATERIAS).delete().eq("id", materia_id).execute()
            if resposta.data:
                return resposta.data[0]
            return materia
        except Exception:
            pass

    nome = materia.get("nome")
    MATERIAS[:] = [item for item in MATERIAS if int(item["id"]) != int(materia_id)]
    SESSOES[:] = [sessao for sessao in SESSOES if sessao.get("materia") != nome]
    return materia


def excluir_materia_por_nome(nome: str):
    nome = (nome or "").strip()
    if not nome:
        return None

    materia = next((item for item in listar_materias() if item.get("nome") == nome), None)
    if materia is None:
        return None

    cliente = cliente_supabase()
    if cliente is not None:
        try:
            resposta = cliente.table(TABELA_MATERIAS).select("*").eq("nome", nome).limit(1).execute()
            if resposta.data:
                materia_banco = resposta.data[0]
                materia_id = materia_banco["id"]
                cliente.table(TABELA_PLANOS).delete().eq("materia_id", materia_id).execute()
                cliente.table(TABELA_SESSOES).delete().eq("materia_id", materia_id).execute()
                cliente.table(TABELA_MATERIAS).delete().eq("id", materia_id).execute()
                return materia_banco
        except Exception:
            pass

    MATERIAS[:] = [item for item in MATERIAS if item.get("nome") != nome]
    SESSOES[:] = [sessao for sessao in SESSOES if sessao.get("materia") != nome]
    return materia


def listar_plano_hoje():
    materias = listar_materias()
    if not materias:
        return []

    materias_ordenadas = sorted(materias, key=lambda item: item["total_minutos"])
    horarios = ["18:30", "19:20", "20:10"]
    plano = []
    for indice, materia in enumerate(materias_ordenadas[:3], start=1):
        plano.append(
            {
                "id": indice,
                "horario": horarios[indice - 1],
                "materia": materia["nome"],
                "tipo": "revisao" if materia["total_minutos"] >= 45 else "projeto",
                "duracao_minutos": 40,
                "meta": f"Continuar {materia['nome']} com base no historico registrado.",
            }
        )
    return plano


def registrar_sessao(sessao: dict) -> dict:
    sessao = dict(sessao)
    cliente = cliente_supabase()
    if cliente is None:
        sessao["id"] = proximo_id_sessao()
        SESSOES.append(sessao)
        return sessao

    try:
        materia = obter_ou_criar_materia_por_nome(sessao["materia"])
        payload = {
            "materia_id": materia["id"],
            "tipo_estudo": sessao["tipo_estudo"],
            "duracao_minutos": sessao["duracao_minutos"],
            "nivel_foco": sessao["nivel_foco"],
            "observacao": sessao.get("observacao"),
            "data_registro": sessao["data_registro"],
        }
        resposta = cliente.table(TABELA_SESSOES).insert(payload).execute()
    except Exception:
        sessao["id"] = proximo_id_sessao()
        SESSOES.append(sessao)
        return sessao

    if resposta.data:
        salvo = resposta.data[0]
        salvo["materia"] = sessao["materia"]
        return normalizar_sessao(salvo)
    return sessao


def cor_por_nome(nome: str) -> str:
    cores = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#0f766e", "#ca8a04"]
    indice = sum(ord(char) for char in nome) % len(cores)
    return cores[indice]


def obter_ou_criar_materia_por_nome(nome: str):
    cliente = cliente_supabase()
    if cliente is None:
        existente = next((materia for materia in MATERIAS if materia["nome"] == nome), None)
        if existente:
            return existente
        return criar_materia(
            {
                "nome": nome,
                "prioridade": "media",
                "cor": cor_por_nome(nome),
                "descricao": None,
            }
        )

    resposta = cliente.table(TABELA_MATERIAS).select("*").eq("nome", nome).limit(1).execute()
    if resposta.data:
        return resposta.data[0]

    criado = cliente.table(TABELA_MATERIAS).insert(
        {
            "nome": nome,
            "prioridade": "media",
            "cor": cor_por_nome(nome),
            "descricao": None,
        }
    ).execute()
    return criado.data[0]


def normalizar_sessao(sessao: dict):
    item = dict(sessao)
    materia = item.get("materia")
    if isinstance(materia, dict):
        item["materia"] = materia.get("nome", "")
    elif not item.get("materia") and isinstance(item.get("materias"), dict):
        item["materia"] = item["materias"].get("nome", "")
    item.pop("materias", None)
    return item
