"""
ASGI config for tripagenda project.

It exposes the ASGI callable as a module-level variable named ``app``.
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tripagenda.settings')

application = get_asgi_application()

from tripagenda.healthcheck import router as main_router
from api.urls import router as api_router

app = FastAPI(
    title="Goatfish",
    description="A demo project. Also, an actual fish with a weird name.",
    version="We aren't doing versions yet. Point oh.",
)

app.include_router(api_router, prefix=f"{settings.API_PREFIX}/{settings.API_VERSION}")
app.include_router(main_router, prefix=f"{settings.API_INTERNAL_PREFIX}")
