"""
ASGI config for tripagenda project.

It exposes the ASGI callable as a module-level variable named ``app``.
"""
import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripagenda.settings")

application = get_asgi_application()

from tripagenda.routers import router as internal_router
from api.routers.city import router as city_router
from api.routers.itinerary import router as itinerary_router
from api.routers.search import router as search_router

app = FastAPI(
    title="Tripagenda",
    description="A travel itinerary generator.",
    version=settings.APP_VERSION,
    redirect_slashes=True,
)

api_prefix = f"{settings.API_PREFIX}/{settings.API_VERSION}"
internal_prefix = f"{settings.API_INTERNAL_PREFIX}"

app.include_router(city_router, prefix=api_prefix)
app.include_router(itinerary_router, prefix=api_prefix)
app.include_router(search_router, prefix=api_prefix)
app.include_router(internal_router, prefix=internal_prefix)
