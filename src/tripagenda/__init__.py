"""Package initialization."""
import logging
import os

from api.clients.openai import OpenAI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripagenda.settings")
logger = logging.getLogger("tripagenda")
oai = OpenAI()

__all__ = ["logger", "oai"]
