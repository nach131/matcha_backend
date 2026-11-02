from app.routes.resource_routes import create_resource_blueprint

notifications_bp = create_resource_blueprint(
    "notifications",
    "/notifications",
    ("id",),
)
