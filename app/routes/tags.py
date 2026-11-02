from app.routes.resource_routes import create_resource_blueprint

tags_bp = create_resource_blueprint(
    "tags",
    "/tags",
    ("id",),
)
