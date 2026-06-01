from flask import current_app, jsonify, request

from backend.storage import obter_usuario_autenticado, usuario_demo


def usuario_atual_ou_erro():
    auth = request.authorization
    if auth:
        usuario = obter_usuario_autenticado(auth.username, auth.password)
        if usuario:
            return usuario, None

    if current_app.config.get("TESTING"):
        return usuario_demo(), None

    return None, (jsonify({"erro": "Faca login para acessar seus dados."}), 401)
