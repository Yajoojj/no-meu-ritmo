from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from backend.schemas import MateriaEntrada
from backend.storage import autenticar_usuario
from backend.storage import atualizar_materia as salvar_atualizacao_materia
from backend.storage import cadastrar_usuario
from backend.storage import criar_materia as salvar_materia
from backend.storage import excluir_materia as remover_materia
from backend.storage import listar_materias as buscar_materias
from backend.storage import obter_materia as buscar_materia

materias_bp = Blueprint("materias", __name__)


def validar_usuario_materias():
    auth = request.authorization
    if auth and autenticar_usuario(auth.username, auth.password):
        return None

    return jsonify({"erro": "Usuario ou senha invalidos para acessar as materias."}), 401, {
        "WWW-Authenticate": 'Basic realm="Materias"'
    }


@materias_bp.post("/cadastro-rapido")
def cadastro_rapido():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400

    usuario, erro = cadastrar_usuario(dados.get("username", ""), dados.get("password", ""))
    if erro:
        return jsonify({"erro": erro}), 422

    return jsonify({"mensagem": "Cadastro criado com sucesso.", "usuario": usuario}), 201


@materias_bp.post("/login")
def login():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400

    username = dados.get("username", "")
    password = dados.get("password", "")
    if not autenticar_usuario(username, password):
        return jsonify({"erro": "Usuario ou senha invalidos."}), 401

    return jsonify({"mensagem": "Login realizado com sucesso.", "usuario": {"username": username}})


@materias_bp.get("/materias")
def listar_materias():
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login
    return jsonify(buscar_materias())


@materias_bp.get("/materias/<int:materia_id>")
def detalhar_materia(materia_id: int):
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    materia = buscar_materia(materia_id)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify(materia)


@materias_bp.post("/materias")
def criar_materia():
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400
    try:
        entrada = MateriaEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados invalidos.", "detalhes": erro.errors()}), 422
    materia = salvar_materia(entrada.model_dump())
    return jsonify({"mensagem": "Materia criada com sucesso.", "materia": materia}), 201


@materias_bp.put("/materias/<int:materia_id>")
def atualizar_materia(materia_id: int):
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400
    try:
        entrada = MateriaEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados invalidos.", "detalhes": erro.errors()}), 422
    materia = salvar_atualizacao_materia(materia_id, entrada.model_dump())
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia atualizada com sucesso.", "materia": materia})


@materias_bp.delete("/materias/<int:materia_id>")
def excluir_materia(materia_id: int):
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    materia = remover_materia(materia_id)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia removida com sucesso.", "materia": materia})
