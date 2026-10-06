def register_routes(app):
    @app.route("/")
    def index():
        return {
            "message": "hello"
        }

    @app.route("/health")
    def health():
        return {
            "success": True,
            "message": "Llegaste aqui Mother F**ck"
        }