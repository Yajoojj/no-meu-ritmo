from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from backend.schemas import MateriaEntrada
from backend.storage import atualizar_materia as salvar_atualizacao_materia
from backend.storage import criar_materia as salvar_materia
from backend.storage import excluir_materia as remover_materia
from backend.storage import listar_materias as buscar_materias
from backend.storage import obter_materia as buscar_materia

materias_bp = Blueprint("materias", __name__)

USUARIO_MATERIAS = "aluno"
SENHA_MATERIAS = "1234"


def validar_usuario_materias():
    auth = request.authorization
    if auth and auth.username == USUARIO_MATERIAS and auth.password == SENHA_MATERIAS:
        return None

    return jsonify({"erro": "Usuario ou senha invalidos para acessar as materias."}), 401, {
        "WWW-Authenticate": 'Basic realm="Materias"'
    }


@materias_bp.get("/materias")
def listar_materias():
    """
    Lista as materias cadastradas.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Lista de materias cadastradas pelo usuario.
      401:
        description: Usuario ou senha invalidos.
    """
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login
    return jsonify(buscar_materias())


@materias_bp.get("/materias/<int:materia_id>")
def detalhar_materia(materia_id: int):
    """
    Busca uma materia pelo ID.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Materia encontrada.
      401:
        description: Usuario ou senha invalidos.
      404:
        description: Materia nao encontrada.
    """
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    materia = buscar_materia(materia_id)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify(materia)


@materias_bp.post("/materias")
def criar_materia():
    """
    Cria uma nova materia com validacao Pydantic.
    ---
    tags:
      - Materias
    parameters:
      - in: body
        name: materia
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              example: Redes
            prioridade:
              type: string
              enum: [baixa, media, alta]
              example: media
            cor:
              type: string
              example: "#2563eb"
            descricao:
              type: string
              example: Revisar conteudo para a prova.
    responses:
      201:
        description: Materia criada com sucesso.
      401:
        description: Usuario ou senha invalidos.
      422:
        description: Dados invalidos.
    """
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
    """
    Atualiza uma materia existente.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Materia atualizada com sucesso.
      401:
        description: Usuario ou senha invalidos.
      404:
        description: Materia nao encontrada.
      422:
        description: Dados invalidos.
    """
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
    """
    Remove uma materia cadastrada.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Materia removida com sucesso.
      401:
        description: Usuario ou senha invalidos.
      404:
        description: Materia nao encontrada.
    """
    erro_login = validar_usuario_materias()
    if erro_login:
        return erro_login

    materia = remover_materia(materia_id)
    if materia is None:
        return jsonify({"erro": "Materia nao encontrada."}), 404
    return jsonify({"mensagem": "Materia removida com sucesso.", "materia": materia})
