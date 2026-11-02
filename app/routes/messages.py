from app.routes.resource_routes import create_resource_blueprint

messages_bp = create_resource_blueprint(
    "messages",
    "/messages",
    ("id",),
)
