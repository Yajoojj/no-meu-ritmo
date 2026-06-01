import os
import secrets

from flask import current_app, jsonify, request

from backend.storage import obter_usuario_autenticado as obter_usuario_storage
from backend.storage import usuario_demo

TEST_USER = {
    "id": 1,
    "username": os.getenv("API_USERNAME", "aluno"),
    "password": os.getenv("API_PASSWORD", "1234"),
    "nome": "Aluno Demo",
}
TOKENS = {}


def modo_demo_ativo() -> bool:
    return os.getenv("DEMO_MODE") == "1"


def usuario_publico(usuario: dict) -> dict:
    return {chave: valor for chave, valor in usuario.items() if chave not in {"password", "senha_hash"}}


def obter_usuario_autenticado(username, password):
    if modo_demo_ativo():
        if username == TEST_USER["username"] and password == TEST_USER["password"]:
            return usuario_publico(TEST_USER)

    return obter_usuario_storage(username, password)


def gerar_token(usuario: dict) -> str:
    token = secrets.token_hex(16)
    TOKENS[token] = usuario_publico(usuario)
    return token


def usuario_atual_ou_erro():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        usuario = TOKENS.get(token)
        if usuario:
            return usuario, None

    auth = request.authorization
    if auth:
        usuario = obter_usuario_autenticado(auth.username, auth.password)
        if usuario:
            return usuario, None

    if modo_demo_ativo() or current_app.config.get("TESTING"):
        return usuario_publico(TEST_USER) if modo_demo_ativo() else usuario_demo(), None

    return None, (jsonify({"erro": "Faca login para acessar seus dados."}), 401)
