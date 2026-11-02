from app.routes.resource_routes import create_resource_blueprint

blocks_bp = create_resource_blueprint(
    "blocks",
    "/blocks",
    ("id",),
)
