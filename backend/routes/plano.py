from flask import Blueprint, jsonify

from backend.data import PLANO_HOJE

plano_bp = Blueprint("plano", __name__)


@plano_bp.get("/plano-hoje")
def listar_plano_hoje():
    """
    Mostra o plano de estudos sugerido para hoje.
    ---
    tags:
      - Plano de estudos
    responses:
      200:
        description: Blocos de estudo sugeridos para o dia.
        schema:
          type: array
          items:
            type: object
            properties:
              horario:
                type: string
              materia:
                type: string
              tipo:
                type: string
              duracao_minutos:
                type: integer
              meta:
                type: string
    """
    return jsonify(PLANO_HOJE)
