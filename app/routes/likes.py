from app.routes.resource_routes import create_resource_blueprint

likes_bp = create_resource_blueprint(
    "likes",
    "/likes",
    ("id",),
)
