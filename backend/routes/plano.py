from flask import Blueprint, jsonify

from backend.storage import listar_plano_hoje as buscar_plano_hoje

plano_bp = Blueprint("plano", __name__)


@plano_bp.get("/plano-hoje")
def listar_plano_hoje():
    """
    Mostra um plano de estudos sugerido com base nas sessoes reais.
    ---
    tags:
      - Plano de estudos
    responses:
      200:
        description: Blocos de estudo sugeridos a partir do historico registrado.
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
    return jsonify(buscar_plano_hoje())
