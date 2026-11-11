"""Authentication helpers for session-protected routes."""

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, cast

from flask import g, jsonify, request

from app.services.sessions import SESSION_COOKIE_NAME, get_session_user_id

P = ParamSpec("P")
R = TypeVar("R")


def require_session(
    view: Callable[P, R],
) -> Callable[P, R]:
    """Reject requests without a valid server-side session cookie."""

    @wraps(view)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        user_id = get_session_user_id(
            request.cookies.get(SESSION_COOKIE_NAME)
        )
        if user_id is None:
            return cast(
                R,
                (
                    jsonify({
                        "success": False,
                        "message": "Authentication required.",
                        "data": None,
                    }),
                    401,
                ),
            )

        g.user_id = user_id
        return view(*args, **kwargs)

    return wrapped
