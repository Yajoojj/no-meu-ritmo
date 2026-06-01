from pathlib import Path

from flasgger import Swagger
from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.landing import LANDING_HTML
from backend.routes.materias import materias_bp
from backend.routes.plano import plano_bp
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
    app.register_blueprint(sessoes_bp, url_prefix="/api")

    @app.get("/")
    def landing_page():
        public_dir = Path(__file__).resolve().parent.parent / "public"
        index_html = public_dir / "index.html"
        if index_html.exists():
            return send_from_directory(public_dir, "index.html")
        return LANDING_HTML

    return app
