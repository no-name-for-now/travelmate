from typing import Any

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel


class UniqueSavedItineraryORM(AbstractBaseModel):
    class Meta:
        db_table = "unique_saved_itinerary"

    user_id = models.IntegerField()
    blob = models.JSONField()


class UniqueSavedItineraryContract(BaseModel):
    """City Climate contract."""

    user_id: int
    blob: Any

    @classmethod
    def from_model(
        cls, instance: UniqueSavedItineraryORM
    ) -> "UniqueSavedItineraryContract":
        """Convert a Django CityClimate model instance to an APICityClimate instance."""
        return cls(
            id=instance.id,
            user_id=instance.city_id,
            blob=instance.blob,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "blob": self.blob,
        }
