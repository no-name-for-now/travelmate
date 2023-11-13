from typing import List

from pydantic import BaseModel


class ItineraryActivityOpenAIContract(BaseModel):
    overnight_city: str
    travel_method: str
    travel_time: str
    morning_activity: str
    afternoon_activity: str
    evening_activity: str


class ItineraryOpenAIContract(BaseModel):
    city: str
    country: str
    num_days: int
    day: str
    activities: List[ItineraryActivityOpenAIContract]
