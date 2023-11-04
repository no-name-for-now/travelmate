from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel
from api.models.unique_search_history import UniqueSearchHistoryORM


class ItineraryORM(AbstractBaseModel):
    """Itinerary model."""

    class Meta:
        db_table = "itineraries"

    unique_search_history = models.ForeignKey(
        UniqueSearchHistoryORM, on_delete=models.CASCADE
    )
    day = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    travel_method = models.CharField(max_length=50)
    travel_time = models.CharField(max_length=50)
    morning_activity = models.CharField(max_length=150)
    afternoon_activity = models.CharField(max_length=150)
    evening_activity = models.CharField(max_length=150)

    @classmethod
    def from_api(
        cls, unique_search_history: "UniqueSearchHistoryORM", model: "ItineraryContract"
    ):
        """
        Return an Itinerary instance from an APIItinerary instance.
        """
        return cls(
            unique_search_history_id=unique_search_history.id,
            day=model.day,
            city=model.city,
            travel_method=model.travel_method,
            travel_time=model.travel_time,
            morning_activity=model.morning_activity,
            afternoon_activity=model.afternoon_activity,
            evening_activity=model.evening_activity,
        )

    def update_from_api(self, api_model: "ItineraryContract"):
        """
        Update the Itinerary Django model from an APIItinerary instance.
        """
        self.day = api_model.day
        self.city = api_model.city
        self.travel_method = api_model.travel_method
        self.travel_time = api_model.travel_time
        self.morning_activity = api_model.morning_activity
        self.afternoon_activity = api_model.afternoon_activity
        self.evening_activity = api_model.evening_activity


# Itinerary contracts
class ItineraryContract(BaseModel):
    """Itinerary contract."""

    day: str
    city: str
    travel_method: str
    travel_time: str
    morning_activity: str
    afternoon_activity: str
    evening_activity: str

    @classmethod
    def from_model(cls, instance: ItineraryORM):
        """
        Convert a Django Itinerary model instance to an APIItinerary instance.
        """
        return cls(
            id=instance.id,
            day=instance.day,
            city=instance.city,
            travel_method=instance.travel_method,
            travel_time=instance.travel_time,
            morning_activity=instance.morning_activity,
            afternoon_activity=instance.afternoon_activity,
            evening_activity=instance.evening_activity,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "day": self.day,
            "city": self.city,
            "travel_method": self.travel_method,
            "travel_time": self.travel_time,
            "morning_activity": self.morning_activity,
            "afternoon_activity": self.afternoon_activity,
            "evening_activity": self.evening_activity,
        }


class APIItinerary(ItineraryContract):
    id: int


# APIItineraryList contracts
class APIItineraryList(BaseModel):
    """API Itinerary List contract."""

    items: List[APIItinerary]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django Itinerary queryset to APIItinerary instances.
        """
        return cls(items=[APIItinerary.from_model(i) for i in qs])
