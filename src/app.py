from flask import Flask

from src.routes import health_bp, orders_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    app.register_blueprint(orders_bp)
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=False)
