from typing import List

from api.models.base import AbstractBaseModel
from api.models.world_cities import WorldCitiesORM
from django.db import models
from pydantic import BaseModel


class CityClimateORM(AbstractBaseModel):
    """City Climate ORM."""

    city = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    month = models.CharField(max_length=15)
    low = models.IntegerField()
    high = models.IntegerField()
    rainfall = models.IntegerField()

    class Meta:
        db_table = "city_climate"
        constraints = [
            models.UniqueConstraint(
                fields=["city_id", "month"],
                name="constraint__unique_city_climate_month",
            )
        ]

    @classmethod
    def from_api(cls, model: "CityClimateContract") -> "CityClimateORM":
        """Create a CityClimateORM object from API data."""
        return cls(
            world_city=model.city_id,
            month=model.month,
            low=model.low,
            high=model.high,
            rainfall=model.rainfall,
        )

    def update_from_api(self, api_model: "CityClimateContract"):
        """Update the CityClimateORM object from API data."""
        self.world_city = api_model.city_id
        self.month = api_model.month
        self.low = api_model.low
        self.high = api_model.high
        self.rainfall = api_model.rainfall


# CityClimate contracts
class CityClimateContract(BaseModel):
    """City Climate contract."""

    city_id: int
    month: str
    low: int
    high: int
    rainfall: int

    @classmethod
    def from_model(cls, instance: CityClimateORM) -> "CityClimateContract":
        """Convert a Django CityClimate model instance to an APICityClimate instance."""
        return cls(
            id=instance.id,
            city_id=instance.city_id,
            month=instance.month,
            low=instance.low,
            high=instance.high,
            rainfall=instance.rainfall,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "month": self.month,
            "low": self.low,
            "high": self.high,
            "rainfall": self.rainfall,
        }


class APICityClimate(CityClimateContract):
    id: int


# APICityClimateList contracts
class APICityClimateList(BaseModel):
    """API City Climate List contract."""

    items: List[APICityClimate]

    @classmethod
    def from_qs(cls, qs):
        """Convert a Django CityClimate queryset to APICityClimate instances."""
        return cls(items=[APICityClimate.from_model(instance) for instance in qs])
