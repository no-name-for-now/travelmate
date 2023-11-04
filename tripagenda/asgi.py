"""
ASGI config for tripagenda project.

It exposes the ASGI callable as a module-level variable named ``app``.
"""
import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripagenda.settings")

application = get_asgi_application()


from django.conf import settings
from fastapi import FastAPI

from api.routers.city import city_router
from api.routers.city import cities_router
from api.routers.itinerary import router as itinerary_router
from api.routers.search import router as search_router
from tripagenda.routers import router as internal_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["15/minute"],
)

app = FastAPI(
    title="Tripagenda",
    description="A travel itinerary generator.",
    version=settings.APP_VERSION,
    redirect_slashes=True,
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

api_prefix = f"{settings.API_PREFIX}/{settings.API_VERSION}"
internal_prefix = f"{settings.API_INTERNAL_PREFIX}"

app.include_router(city_router, prefix=api_prefix)
app.include_router(cities_router, prefix=api_prefix)
app.include_router(itinerary_router, prefix=api_prefix)
app.include_router(search_router, prefix=api_prefix)
app.include_router(internal_router, prefix=internal_prefix)
