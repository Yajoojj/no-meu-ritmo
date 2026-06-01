from flask import Blueprint, jsonify

from backend.storage import listar_materias as buscar_materias

materias_bp = Blueprint("materias", __name__)


@materias_bp.get("/materias")
def listar_materias():
    """
    Lista as materias criadas a partir das sessoes registradas.
    ---
    tags:
      - Materias
    responses:
      200:
        description: Lista de materias reais derivadas do historico de estudo.
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
    return jsonify(buscar_materias())
