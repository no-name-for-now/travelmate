from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel
from api.models.world_cities import WorldCitiesORM


class ItineraryItemsORM(AbstractBaseModel):
    class Meta:
        db_table = "itinerary_items"

    city = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    tag = models.CharField(max_length=25)
    duration_minutes = models.IntegerField()
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    description = models.CharField(max_length=250, null=True)

    @classmethod
    def from_oai(cls, oai_model):
        """Create a CityClimateORM object from OpenAI data."""
        city = WorldCitiesORM.objects.filter(city=oai_model.get("city", None)).first()
        city_id = city.id if city else None

        return cls(
            city_id=city_id,
            item=oai_model.get("item"),
            tag=oai_model.get("tag"),
            duration_minutes=oai_model.get("duration_minutes"),
        )


# CityClimate contracts
class ItineraryItemsContract(BaseModel):
    """City Climate contract."""

    city_id: int
    item: str
    tag: str
    duration_minutes: int

    @classmethod
    def from_model(cls, instance: ItineraryItemsORM) -> "ItineraryItemsContract":
        """Convert a Django CityClimate model instance to an APICityClimate instance."""
        return cls(
            id=instance.id,
            city_id=instance.city_id,
            item=instance.item,
            tag=instance.tag,
            duration_minutes=instance.duration_minutes,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "item": self.item,
            "tag": self.tag,
            "duration_minutes": self.duration_minutes,
        }


class APIItineraryItems(ItineraryItemsContract):
    id: int


# APICityClimateList contracts
class APIItineraryItemsList(BaseModel):
    """API City Climate List contract."""

    items: List[APIItineraryItems]

    @classmethod
    def from_qs(cls, qs):
        """Convert a Django APIItineraryItems queryset to APIItineraryItems instances."""
        return cls(items=[APIItineraryItems.from_model(instance) for instance in qs])
