from app.routes.resource_routes import create_resource_blueprint

profile_visits_bp = create_resource_blueprint(
    "profile_visits",
    "/profile-visits",
    ("id",),
)
