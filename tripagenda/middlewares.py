import base64
import secrets

from django.conf import settings
from fastapi import status
from fastapi.security import HTTPBasic
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from api.utils.http import Error


security = HTTPBasic()
correct_username_bytes = settings.API_BASIC_AUTH_USERNAME.encode("utf8")
correct_password_bytes = settings.API_BASIC_AUTH_PASSWORD.encode("utf8")
correct_internal_username_bytes = settings.API_INTERNAL_BASIC_AUTH_USERNAME.encode(
    "utf8"
)
correct_internal_password_bytes = settings.API_INTERNAL_BASIC_AUTH_PASSWORD.encode(
    "utf8"
)


class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        from tripagenda import logger

        logger.info(f"request.url.path: {request.url.path}")
        if request.url.path.startswith(settings.API_INTERNAL_PREFIX):
            if not request.headers.get("Authorization"):
                return Error(
                    code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    instance=request.url.path,
                )
            try:
                scheme, credentials = request.headers["Authorization"].split()
                assert scheme.lower() == "basic"
                decoded_credentials = base64.b64decode(credentials).decode("utf-8")
                username, password = decoded_credentials.split(":")
                assert secrets.compare_digest(
                    username.encode("utf-8"), correct_internal_username_bytes
                )
                assert secrets.compare_digest(
                    password.encode("utf-8"), correct_internal_password_bytes
                )
            except (ValueError, AssertionError):
                return Error(
                    code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    instance=request.url.path,
                )
        elif request.url.path.startswith(settings.API_PREFIX):
            if not request.headers.get("Authorization"):
                return Error(
                    code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    instance=request.url.path,
                )
            try:
                scheme, credentials = request.headers["Authorization"].split()
                assert scheme.lower() == "basic"
                decoded_credentials = base64.b64decode(credentials).decode("utf-8")
                username, password = decoded_credentials.split(":")
                assert secrets.compare_digest(
                    username.encode("utf-8"), correct_username_bytes
                )
                assert secrets.compare_digest(
                    password.encode("utf-8"), correct_password_bytes
                )
            except (
                ValueError,
                AssertionError,
            ):
                return Error(
                    code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized",
                    instance=request.url.path,
                )
        else:
            return Error(
                code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown API prefix",
                instance=request.url.path,
            )
        return await call_next(request)
