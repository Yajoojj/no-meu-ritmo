from datetime import date

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from backend.data import SESSOES, proximo_id_sessao
from backend.schemas import SessaoEstudoEntrada

sessoes_bp = Blueprint("sessoes", __name__)


@sessoes_bp.get("/sessoes")
def listar_sessoes():
    """
    Lista as sessões de estudo registradas.
    ---
    tags:
      - Sessões
    responses:
      200:
        description: Histórico em memória das sessões cadastradas.
    """
    return jsonify(SESSOES)


@sessoes_bp.post("/sessoes")
def registrar_sessao():
    """
    Registra uma nova sessão de estudo com validação.
    ---
    tags:
      - Sessões
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
              example: Programação Web
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
              example: Finalizei a parte de integração com a API.
    responses:
      201:
        description: Sessão registrada com sucesso.
      400:
        description: JSON inválido ou ausente.
      422:
        description: Dados enviados não passaram pela validação.
    """
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie um JSON válido no corpo da requisição."}), 400

    try:
        entrada = SessaoEstudoEntrada.model_validate(dados)
    except ValidationError as erro:
        return jsonify({"erro": "Dados inválidos.", "detalhes": erro.errors()}), 422

    sessao = entrada.model_dump()
    sessao["id"] = proximo_id_sessao()
    sessao["data_registro"] = date.today().isoformat()
    SESSOES.append(sessao)

    return jsonify({"mensagem": "Sessão registrada com sucesso.", "sessao": sessao}), 201
