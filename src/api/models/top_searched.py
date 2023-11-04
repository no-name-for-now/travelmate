from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel


class TopSearchedContract(BaseModel):
    """Top Searched contract."""

    city: str
    country: str
    itinerary_length: int
    number_of_searches: int

    @classmethod
    def from_model(cls, instance: Dict[str, Any]):
        """
        Convert an aggregated Django UniqueSearchHistory model instance to a TopSearchedContract instance.
        """
        return cls(
            city=instance["city"],
            country=instance["country"],
            itinerary_length=instance["num_days"],
            number_of_searches=instance["number_of_searches"],
        )

    def to_dict(self):
        return {
            "city": self.city,
            "country": self.country,
            "itinerary_length": self.itinerary_length,
            "number_of_searches": self.number_of_searches,
        }


# APITopSearchedList contracts
class APITopSearchedList(BaseModel):
    """API Top Searched List contract."""

    items: List[TopSearchedContract]

    @classmethod
    def from_qs(cls, qs):
        """Convert an aggregated Django UniqueSearchHistory queryset to TopSearchedContract instances."""
        return cls(items=[TopSearchedContract.from_model(i) for i in qs])
