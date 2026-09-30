from flask import Flask


def test_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return {
            "success": True,
            "message": "Matcha jajajaja es ta funcionado"
        }

    @app.route("/health")
    def health():
        return {
            "success": True,
            "message": "Llegaste aqui Mother F**ck"
        }

    return app
