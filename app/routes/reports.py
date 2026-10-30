from app.routes.resource_routes import create_resource_blueprint

reports_bp = create_resource_blueprint(
    "reports",
    "/reports",
    ("id",),
)
