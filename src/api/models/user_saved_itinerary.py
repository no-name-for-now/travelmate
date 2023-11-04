from datetime import date
from typing import List

from api.models.base import AbstractBaseModel
from api.models.unique_search_history import UniqueSearchHistoryORM
from django.db import models
from pydantic import BaseModel


class UserSavedItineraryORM(AbstractBaseModel):
    """User Saved Itinerary model."""

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "unique_search_history_id", "from_date", "to_date"],
                name="constraint__user_saved_itinerary",
            )
        ]
        db_table = "user_saved_itinerary"

    user_id = models.IntegerField()
    unique_search_history = models.ForeignKey(
        UniqueSearchHistoryORM, on_delete=models.CASCADE
    )
    from_date = models.DateField()
    to_date = models.DateField()

    @classmethod
    def from_api(
        cls,
        model: "UserSavedItineraryContract",
    ):
        """
        Return a UserSavedItinerary instance from an APIUserSavedItinerary instance.
        """
        return cls(
            user_id=model.user_id,
            unique_search_history_id=model.unique_search_history_id,
            from_date=model.from_date,
            to_date=model.to_date,
        )

    def update_from_api(self, api_model: "UserSavedItineraryContract"):
        """
        Update the UserSavedItinerary Django model from an APIUserSavedItinerary instance.
        """
        self.user_id = api_model.user_id
        self.unique_search_history_id = api_model.unique_search_history_id
        self.from_date = api_model.from_date
        self.to_date = api_model.to_date


# UserSavedItinerary contracts
class UserSavedItineraryContract(BaseModel):
    """User Saved Itinerary contract."""

    user_id: int
    unique_search_history_id: int
    from_date: date
    to_date: date

    @classmethod
    def from_model(cls, instance: UserSavedItineraryORM):
        """
        Convert a Django UserSavedItinerary model instance to an APIUserSavedItinerary instance.
        """
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            unique_search_history_id=instance.unique_search_history_id,
            from_date=instance.from_date,
            to_date=instance.to_date,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "unique_search_history_id": self.unique_search_history_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
        }


class APIUserSavedItinerary(UserSavedItineraryContract):
    id: int


# APIUserSavedItineraryList contracts
class APIUserSavedItineraryList(BaseModel):
    """API User Saved Itinerary List contract."""

    items: List[APIUserSavedItinerary]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UserSavedItinerary queryset to APIUserSavedItinerary instances.
        """
        return cls(items=[APIUserSavedItinerary.from_model(i) for i in qs])
