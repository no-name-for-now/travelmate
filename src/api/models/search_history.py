from typing import List

from api.models.base import AbstractBaseModel
from api.models.unique_search_history import UniqueSearchHistoryORM
from django.db import models
from pydantic import BaseModel


class SearchHistoryORM(AbstractBaseModel):
    """Search History model."""

    class Meta:
        db_table = "search_history"

    unique_search_history = models.ForeignKey(
        UniqueSearchHistoryORM, on_delete=models.CASCADE
    )

    @classmethod
    def from_api(cls, unique_search_history: "UniqueSearchHistoryORM"):
        """
        Return a SearchHistory instance from an APIUniqueSearchHistory instance.
        """
        return cls(
            unique_search_history_id=unique_search_history.id,
        )

    def update_from_api(self, api_model: "UniqueSearchHistoryORM"):
        """
        Update the SearchHistory Django model from an APIUniqueSearchHistory instance.
        """
        self.unique_search_history_id = api_model.id


# SearchHistory contracts
class SearchHistoryContract(BaseModel):
    """Search History contract."""

    unique_search_history_id: int

    @classmethod
    def from_model(cls, instance: SearchHistoryORM):
        """
        Convert a Django SearchHistory model instance to an APISearchHistory instance.
        """
        return cls(
            id=instance.id,
            unique_search_history_id=instance.unique_search_history_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "unique_search_history_id": self.unique_search_history_id,
        }


class APISearchHistory(SearchHistoryContract):
    id: int


# APISearchHistoryList contracts
class APISearchHistoryList(BaseModel):
    """API Search History List contract."""

    items: List[APISearchHistory]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django SearchHistory queryset to APISearchHistory instances.
        """
        return cls(items=[APISearchHistory.from_model(i) for i in qs])
