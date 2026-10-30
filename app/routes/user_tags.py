from app.routes.resource_routes import create_resource_blueprint

user_tags_bp = create_resource_blueprint(
    "user_tags",
    "/user-tags",
    ("user_id", "tag_id"),
)
