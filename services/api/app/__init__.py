from flask import Flask

from .config import load_settings


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SETTINGS"] = settings = load_settings()
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB uploads

    from .routes.core import bp as core_bp
    app.register_blueprint(core_bp)
    from .routes.batches import bp as batches_bp
    app.register_blueprint(batches_bp)
    from .routes.money import bp as money_bp
    app.register_blueprint(money_bp)
    from .routes.activity import bp as activity_bp
    app.register_blueprint(activity_bp)

    @app.after_request
    def cors(resp):
        resp.headers["Access-Control-Allow-Origin"] = settings.web_origin
        resp.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Vary"] = "Origin"
        return resp

    return app
