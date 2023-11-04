"""Package initialization."""
import logging

from api.clients.openai import OpenAI


logger = logging.getLogger("tripagenda")
oai = OpenAI()

__all__ = ["logger", "oai"]
