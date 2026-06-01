from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from backend.auth import gerar_token
from backend.auth import obter_usuario_autenticado
from backend.auth import usuario_atual_ou_erro
from backend.schemas import MateriaEntrada
from backend.storage import autenticar_usuario
from backend.storage import atualizar_materia as salvar_atualizacao_materia
from backend.storage import cadastrar_usuario
from backend.storage import criar_materia as salvar_materia
from backend.storage import excluir_materia as remover_materia
from backend.storage import excluir_materia_por_nome as remover_materia_por_nome
from backend.storage import listar_materias as buscar_materias
from backend.storage import obter_materia as buscar_materia

materias_bp = Blueprint("materias", __name__)


def validar_usuario_materias():
    auth = request.authorization
    if auth and autenticar_usuario(auth.username, auth.password):
        return None

    # Sem o header WWW-Authenticate para impedir o pop-up nativo do navegador.
    # A tela de acesso do frontend cuida do login.
    return jsonify({"erro": "Faca login para acessar as materias."}), 401


@materias_bp.post("/cadastro-rapido")
def cadastro_rapido():
    """
    Cria um usuario simples para demonstracao e retorna token de acesso.
    ---
    tags:
      - Autenticacao
    parameters:
      - in: body
        name: usuario
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: aluno
            password:
              type: string
              example: "1234"
    responses:
      201:
        description: Cadastro criado com sucesso e token retornado.
      422:
        description: Usuario invalido ou ja cadastrado.
    """
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400

    usuario, erro = cadastrar_usuario(dados.get("username", ""), dados.get("password", ""))
    if erro:
        return jsonify({"erro": erro}), 422

    token = gerar_token(usuario)
    return jsonify({"mensagem": "Cadastro criado com sucesso.", "usuario": usuario, "token": token}), 201


@materias_bp.post("/login")
def login():
    """
    Autentica o usuario e retorna um token Bearer.
    ---
    tags:
      - Autenticacao
    parameters:
      - in: body
        name: credenciais
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: aluno
            password:
              type: string
              example: "1234"
    responses:
      200:
        description: Login realizado com sucesso.
      401:
        description: Usuario ou senha invalidos.
    """
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400

    username = dados.get("username", "")
    password = dados.get("password", "")
    usuario = obter_usuario_autenticado(username, password)
    if not usuario:
        return jsonify({"erro": "Usuario ou senha invalidos."}), 401

    token = gerar_token(usuario)
    return jsonify({"mensagem": "Login realizado com sucesso.", "usuario": usuario, "token": token})


@materias_bp.get("/materias")
def listar_materias():
    """
    Lista as materias cadastradas e seus totais de estudo.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Lista de materias cadastradas, incluindo totais calculados a partir das sessoes.
    """
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    return jsonify(buscar_materias(usuario))


@materias_bp.get("/materias/<int:materia_id>")
def detalhar_materia(materia_id: int):
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    materia = buscar_materia(materia_id, usuario)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify(materia)


@materias_bp.post("/materias")
def criar_materia():
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400
    try:
        entrada = MateriaEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados invalidos.", "detalhes": erro.errors()}), 422
    materia = salvar_materia(entrada.model_dump(), usuario)
    return jsonify({"mensagem": "Materia criada com sucesso.", "materia": materia}), 201


@materias_bp.put("/materias/<int:materia_id>")
def atualizar_materia(materia_id: int):
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400
    try:
        entrada = MateriaEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados invalidos.", "detalhes": erro.errors()}), 422
    materia = salvar_atualizacao_materia(materia_id, entrada.model_dump(), usuario)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia atualizada com sucesso.", "materia": materia})


@materias_bp.delete("/materias/<int:materia_id>")
def excluir_materia(materia_id: int):
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    materia = remover_materia(materia_id, usuario)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia removida com sucesso.", "materia": materia})


@materias_bp.delete("/materias-por-nome/<path:nome>")
def excluir_materia_por_nome(nome: str):
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    materia = remover_materia_por_nome(nome, usuario)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia removida com sucesso.", "materia": materia})
