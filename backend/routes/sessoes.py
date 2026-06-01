from datetime import date

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from backend.auth import usuario_atual_ou_erro
from backend.schemas import SessaoEstudoEntrada
from backend.storage import listar_sessoes as buscar_sessoes
from backend.storage import registrar_sessao as salvar_sessao

sessoes_bp = Blueprint("sessoes", __name__)


@sessoes_bp.get("/sessoes")
def listar_sessoes():
    """
    Lista as sessoes de estudo registradas.
    ---
    tags:
      - Sessoes
    responses:
      200:
        description: Historico das sessoes cadastradas, vindo do Supabase quando configurado ou da memoria local.
    """
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro
    return jsonify(buscar_sessoes(usuario))


@sessoes_bp.post("/sessoes")
def registrar_sessao():
    """
    Registra uma nova sessao de estudo com validacao Pydantic.
    ---
    tags:
      - Sessoes
    parameters:
      - in: body
        name: sessao
        required: true
        schema:
          type: object
          required:
            - materia
            - tipo_estudo
            - duracao_minutos
            - nivel_foco
          properties:
            materia:
              type: string
              example: Programacao Web
            tipo_estudo:
              type: string
              enum: [leitura, revisao, exercicios, projeto]
              example: projeto
            duracao_minutos:
              type: integer
              example: 45
            nivel_foco:
              type: integer
              example: 4
            observacao:
              type: string
              example: Finalizei a parte de integracao com a API.
    responses:
      201:
        description: Sessao registrada com sucesso.
      400:
        description: JSON invalido ou ausente.
      422:
        description: Dados enviados nao passaram pela validacao.
    """
    usuario, erro = usuario_atual_ou_erro()
    if erro:
        return erro

    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON valido no corpo da requisicao."}), 400

    try:
        entrada = SessaoEstudoEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados invalidos.", "detalhes": erro.errors()}), 422

    sessao = entrada.model_dump()
    sessao["data_registro"] = date.today().isoformat()
    sessao = salvar_sessao(sessao, usuario)

    return jsonify({"mensagem": "Sessao registrada com sucesso.", "sessao": sessao}), 201
