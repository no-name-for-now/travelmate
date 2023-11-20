from typing import Annotated
from typing import List

from pydantic import BaseModel
from pydantic import Field


class ItineraryItem(BaseModel):
    item: str  # Description of the itinerary item
    tag: str  # An optional tag for the item
    duration_minutes: Annotated[
        int, Field(ge=0)
    ]  # Time in minutes, must be non-negative


class CityItemOpenAIContract(BaseModel):
    name: str
    itinerary: List[ItineraryItem]
