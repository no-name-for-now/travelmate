from fastapi.responses import JSONResponse

from api.models.http import APIError


responses = {
    400: {"model": APIError, "description": "Bad request."},
    401: {"model": APIError, "description": "Unauthorized."},
    403: {"model": APIError, "description": "Forbidden."},
    404: {"model": APIError, "description": "Not found."},
    405: {"model": APIError, "description": "Method not allowed."},
    406: {"model": APIError, "description": "Not acceptable."},
    409: {"model": APIError, "description": "Conflict."},
    415: {"model": APIError, "description": "Unsupported media type."},
    422: {"model": APIError, "description": "Unprocessable entity."},
    500: {"model": APIError, "description": "Internal server error."},
    503: {"model": APIError, "description": "Service unavailable."},
}


def Error(code, detail, instance) -> JSONResponse:
    """Return an error response."""
    return JSONResponse(
        status_code=code,
        content={
            "detail": detail,
            "code": code,
            "type": responses[code]["description"],
            "instance": instance,
        },
    )
