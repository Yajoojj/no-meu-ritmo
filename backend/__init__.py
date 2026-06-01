from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from backend.landing import carregar_landing
from backend.routes.materias import materias_bp
from backend.routes.plano import plano_bp
from backend.routes.relatorios import relatorios_bp
from backend.routes.sessoes import sessoes_bp


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    CORS(app)

    app.config["SWAGGER"] = {
        "title": "No Meu Ritmo! API",
        "uiversion": 3,
        "description": "API simples para organizar estudos, criada para atividade universitária.",
    }
    Swagger(app)

    app.register_blueprint(materias_bp, url_prefix="/api")
    app.register_blueprint(plano_bp, url_prefix="/api")
    app.register_blueprint(relatorios_bp, url_prefix="/api")
    app.register_blueprint(sessoes_bp, url_prefix="/api")

    @app.get("/")
    def landing_page():
        return carregar_landing()

    return app
