from typing import List

from api.models.base import AbstractBaseModel
from django.db import models
from pydantic import BaseModel


class UniqueSearchHistoryORM(AbstractBaseModel):
    """Unique Search History model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "specific_places", "num_days"],
                name="constraint__unique_search_history",
            )
        ]
        db_table = "unique_search_history"

    country = models.CharField(max_length=50)
    specific_places = models.CharField(max_length=100)
    num_days = models.IntegerField()

    @classmethod
    def from_api(cls, model: "UniqueSearchHistoryContract"):
        """
        Return a UniqueSearchHistory instance from an APIUniqueSearchHistory instance.
        """
        return cls(
            country=model.country,
            specific_places=model.specific_places,
            num_days=model.num_days,
        )

    def update_from_api(self, api_model: "UniqueSearchHistoryContract"):
        """
        Update the UniqueSearchHistory Django model from an APIUniqueSearchHistory instance.
        """
        self.country = api_model.country
        self.specific_places = api_model.specific_places
        self.num_days = api_model.num_days


# UniqueSearchHistory contracts
class UniqueSearchHistoryContract(BaseModel):
    """Unique Search History contract."""

    country: str
    specific_places: str
    num_days: int

    @classmethod
    def from_model(cls, instance: UniqueSearchHistoryORM):
        """
        Convert a Django UniqueSearchHistory model instance to an APIUniqueSearchHistory instance.
        """
        return cls(
            id=instance.id,
            country=instance.country,
            specific_places=instance.specific_places,
            num_days=instance.num_days,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "country": self.country,
            "specific_places": self.specific_places,
            "num_days": self.num_days,
        }


class APIUniqueSearchHistory(UniqueSearchHistoryContract):
    id: int


# APIUniqueSearchHistoryList contracts
class APIUniqueSearchHistoryList(BaseModel):
    """API Unique Search History List contract."""

    items: List[APIUniqueSearchHistory]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UniqueSearchHistory queryset to APIUniqueSearchHistory instances.
        """
        return cls(items=[APIUniqueSearchHistory.from_model(i) for i in qs])
