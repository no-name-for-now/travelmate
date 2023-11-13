from typing import List

from pydantic import BaseModel


class CityClimateOpenAIContract(BaseModel):
    """City Climate response from OpenAI contract."""

    city: str
    month: List[str]
    low: List[float]
    high: List[float]
    rainfall: List[float]
