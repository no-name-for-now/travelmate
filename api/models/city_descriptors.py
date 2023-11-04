from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel
from api.models.world_cities import WorldCitiesORM


class CityDescriptorsORM(AbstractBaseModel):
    """City Descriptors model."""

    class Meta:
        db_table = "city_descriptor"

    city = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    city_description = models.CharField(max_length=2000)

    @classmethod
    def from_api(cls, model: "CityDescriptorsContract"):
        """
        Return a CityDescriptors instance from an APICityDescriptors instance.
        """
        return cls(
            city_id=model.city_id,
            city_description=model.city_description,
        )

    def update_from_api(self, api_model: "CityDescriptorsContract"):
        """
        Update the CityDescriptors Django model from an APICityDescriptors instance.
        """
        self.city_id = api_model.city_id
        self.city_description = api_model.city_description


# CityDescriptors contracts
class CityDescriptorsContract(BaseModel):
    """City Descriptors contract."""

    city_id: int
    city_description: str

    @classmethod
    def from_model(cls, instance: CityDescriptorsORM):
        """
        Convert a Django CityDescriptors model instance to an APICityDescriptors instance.
        """
        return cls(
            id=instance.id,
            city_id=instance.city_id,
            city_description=instance.city_description,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "city_description": self.city_description,
        }


class APICityDescriptors(CityDescriptorsContract):
    id: int


# APICityDescriptorsList contracts
class APICityDescriptorsList(BaseModel):
    """API City Descriptors List contract."""

    items: List[APICityDescriptors]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django CityDescriptors queryset to APICityDescriptors instances.
        """
        return cls(items=[APICityDescriptors.from_model(i) for i in qs])
