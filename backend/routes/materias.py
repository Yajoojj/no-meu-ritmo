from flask import Blueprint, jsonify

from backend.data import MATERIAS

materias_bp = Blueprint("materias", __name__)


@materias_bp.get("/materias")
def listar_materias():
    """
    Lista as matérias cadastradas no organizador.
    ---
    tags:
      - Matérias
    responses:
      200:
        description: Lista de matérias disponíveis para estudo.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              prioridade:
                type: string
              descricao:
                type: string
    """
    return jsonify(MATERIAS)
