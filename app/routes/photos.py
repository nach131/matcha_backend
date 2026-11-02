from app.routes.resource_routes import create_resource_blueprint

photos_bp = create_resource_blueprint(
    "photos",
    "/photos",
    ("id",),
)
