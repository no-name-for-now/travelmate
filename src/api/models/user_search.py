from datetime import date
from typing import List

from pydantic import BaseModel


class UserSearchContract(BaseModel):
    """User Search contract."""

    user_id: int
    unique_search_history_id: int
    from_date: date
    to_date: date
    country: str
    city: str
    num_days: int

    @classmethod
    def from_model(
        cls,
        instance,
    ):
        """
        Convert a Django UserSavedItinerary model instance to an APIUserSavedItinerary instance.
        """
        return cls(
            id=instance.id,
            user_id=instance.user_id,
            unique_search_history_id=instance.unique_search_history_id,
            from_date=instance.from_date,
            to_date=instance.to_date,
            country=instance.unique_search_history.country,
            city=instance.unique_search_history.city,
            num_days=instance.unique_search_history.num_days,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "unique_search_history_id": self.unique_search_history_id,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "country": self.country,
            "city": self.city,
            "num_days": self.num_days,
        }


class APIUserSearch(UserSearchContract):
    id: int


# APIUserSearchList contracts
class APIUserSearchList(BaseModel):
    """API User Search List contract."""

    items: List[APIUserSearch]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django UserSearch queryset to APIUserSearch instances.
        """
        return cls(items=[APIUserSearch.from_model(i) for i in qs])
