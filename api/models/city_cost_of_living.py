from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel
from api.models.world_cities import WorldCitiesORM


class CityCostOfLivingORM(AbstractBaseModel):
    """City Cost of Living model."""

    city = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)
    sub_category = models.CharField(max_length=200)
    cost = models.FloatField()
    currency = models.CharField(max_length=200, default="EUR")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["city_id", "category", "sub_category"],
                name="constraint__unique_city_id_category_sub_category",
            )
        ]
        db_table = "city_cost_of_living"

    @classmethod
    def from_api(cls, model: "CityCostOfLivingContract"):
        """
        Return a CityCostOfLiving instance from an APICityCostOfLiving instance.
        """
        return cls(
            city_id=model.city_id,
            category=model.category,
            sub_category=model.sub_category,
            cost=model.cost,
            currency=model.currency,
        )

    def update_from_api(self, api_model: "CityCostOfLivingContract"):
        """
        Update the CityCostOfLiving Django model from an APICityCostOfLiving instance.
        """
        self.city_id = api_model.city_id
        self.category = api_model.category
        self.sub_category = api_model.sub_category
        self.cost = api_model.cost
        self.currency = api_model.currency


class CityCostOfLivingContract(BaseModel):
    """City Cost of Living contract."""

    city_id: int
    category: str
    sub_category: str
    cost: float
    currency: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "city_id": 1,
                "category": "Restaurant",
                "sub_category": "Meal, Inexpensive Restaurant",
                "cost": 10.00,
                "currency": "EUR",
            }
        }

    @classmethod
    def from_model(cls, instance: CityCostOfLivingORM):
        """
        Convert a Django CityCostOfLiving model instance to an APICityCostOfLiving instance.
        """
        return cls(
            city_id=instance.city_id,
            category=instance.category,
            sub_category=instance.sub_category,
            cost=instance.cost,
            currency=instance.currency,
        )

    def to_dict(self):
        return {
            "city_id": self.city_id,
            "category": self.category,
            "sub_category": self.sub_category,
            "cost": self.cost,
            "currency": self.currency,
        }


class APICityCostOfLiving(CityCostOfLivingContract):
    """City Cost of Living API model."""

    id: int


class APICityCostOfLivingList(BaseModel):
    """API City Cost of Living List contract."""

    items: List[APICityCostOfLiving]

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "city_id": 1,
                        "category": "Restaurant",
                        "sub_category": "Meal, Inexpensive Restaurant",
                        "cost": 10.00,
                        "currency": "EUR",
                    }
                ],
            }
        }

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django CityCostOfLiving queryset to APICityCostOfLiving instances.
        """
        return cls(items=[APICityCostOfLiving.from_model(i) for i in qs])
