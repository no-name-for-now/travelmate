from typing import List

from pydantic import BaseModel


class ItineraryActivityOpenAIContract(BaseModel):
    day: str
    city: str
    travel_method: str
    travel_time: str
    morning_activity: str
    afternoon_activity: str
    evening_activity: str


class ItineraryOpenAIContract(BaseModel):
    city: str
    country: str
    num_days: int
    activities: List[ItineraryActivityOpenAIContract]
