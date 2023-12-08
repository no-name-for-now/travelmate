from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel
from api.models.world_cities import WorldCitiesORM


class GygCityMapORM(AbstractBaseModel):
    class Meta:
        db_table = "gyg_city_map"

    city = models.ForeignKey(WorldCitiesORM, on_delete=models.CASCADE)
    gyg_id = models.IntegerField()


class GygCityMapContract(BaseModel):
    """City Climate contract."""

    city_id: int
    gyg_id: int

    @classmethod
    def from_model(cls, instance: GygCityMapORM) -> "GygCityMapContract":
        return cls(
            id=instance.id,
            city_id=instance.city_id,
            gyg_id=instance.gyg_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city_id": self.city_id,
            "gyg_id": self.gyg_id,
        }
