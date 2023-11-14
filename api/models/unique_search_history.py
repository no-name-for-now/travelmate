from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel


class UniqueSearchHistoryORM(AbstractBaseModel):
    """Unique Search History model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "city", "num_days"],
                name="constraint__unique_search_history",
            )
        ]
        db_table = "unique_search_history"

    country = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    num_days = models.IntegerField()

    @classmethod
    def from_api(cls, model: "UniqueSearchHistoryContract"):
        """
        Return a UniqueSearchHistory instance from an APIUniqueSearchHistory instance.
        """
        if isinstance(model, dict):
            model = UniqueSearchHistoryContract(**model)
        return cls(
            country=model.country,
            city=model.city,
            num_days=model.num_days,
        )

    def update_from_api(self, api_model: "UniqueSearchHistoryContract"):
        """
        Update the UniqueSearchHistory Django model from an APIUniqueSearchHistory instance.
        """
        self.country = api_model.country
        self.city = api_model.city
        self.num_days = api_model.num_days


# UniqueSearchHistory contracts
class UniqueSearchHistoryContract(BaseModel):
    """Unique Search History contract."""

    country: str
    city: str
    num_days: int

    @classmethod
    def from_model(cls, instance: UniqueSearchHistoryORM):
        """
        Convert a Django UniqueSearchHistory model instance to an APIUniqueSearchHistory instance.
        """
        return cls(
            id=instance.id,
            country=instance.country,
            city=instance.city,
            num_days=instance.num_days,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "country": self.country,
            "city": self.city,
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
