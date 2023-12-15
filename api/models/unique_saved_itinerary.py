from typing import Any

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel


class UniqueSavedItineraryORM(AbstractBaseModel):
    class Meta:
        db_table = "unique_saved_itinerary"

    user_id = models.IntegerField()
    blob = models.JSONField()
    city = models.CharField(null=True)
    country = models.CharField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


class UniqueSavedItineraryContract(BaseModel):
    """City Climate contract."""

    user_id: int
    blob: Any
    city: str
    country: str
    start_date: str
    end_date: str

    @classmethod
    def from_model(
        cls, instance: UniqueSavedItineraryORM
    ) -> "UniqueSavedItineraryContract":
        """Convert a Django CityClimate model instance to an APICityClimate instance."""
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            blob=instance.blob,
            city=instance.city,
            country=instance.country,
            start_date=instance.start_date,
            end_date=instance.end_date,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "blob": self.blob,
            "city": self.city,
            "country": self.country,
            "start_date": self.country,
            "end_date": self.country,
        }
