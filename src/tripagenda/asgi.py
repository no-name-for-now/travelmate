"""
ASGI config for tripagenda project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from fastapi import FastAPI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tripagenda.settings')

application = get_asgi_application()

from api.urls import router as main_router

app = FastAPI(
    title="Goatfish",
    description="A demo project. Also, an actual fish with a weird name.",
    version="We aren't doing versions yet. Point oh.",
)

app.include_router(main_router, prefix="/api")
