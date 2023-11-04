from typing import List

from django.db import models
from pydantic import BaseModel

from api.models.base import AbstractBaseModel


class WorldCitiesORM(AbstractBaseModel):
    """World Cities model."""

    class Meta:
        db_table = "world_cities"

    city = models.CharField(max_length=50)
    city_ascii = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    lat = models.FloatField()
    lng = models.FloatField()
    population = models.IntegerField()
    use_on_app = models.BooleanField(default=False)

    @classmethod
    def from_api(cls, model: "WorldCitiesContract"):
        """
        Return a WorldCities instance from an APIWorldCities instance.
        """
        return cls(
            city=model.city,
            city_ascii=model.city_ascii,
            country=model.country,
            iso2=model.iso2,
            iso3=model.iso3,
            lat=model.lat,
            lng=model.lng,
            population=model.population,
            use_on_app=model.use_on_app,
        )

    def update_from_api(self, api_model: "WorldCitiesContract"):
        """
        Update the WorldCities Django model from an APIWorldCities instance.
        """
        self.city = api_model.city
        self.city_ascii = api_model.city_ascii
        self.country = api_model.country
        self.iso2 = api_model.iso2
        self.iso3 = api_model.iso3
        self.lat = api_model.lat
        self.lng = api_model.lng
        self.population = api_model.population
        self.use_on_app = api_model.use_on_app


# WorldCities contracts
class WorldCitiesContract(BaseModel):
    """World Cities contract."""

    city: str
    city_ascii: str
    country: str
    iso2: str
    iso3: str
    lat: float
    lng: float
    population: int
    use_on_app: bool

    @classmethod
    def from_model(cls, instance: WorldCitiesORM):
        """
        Convert a Django WorldCities model instance to an APIWorldCities instance.
        """
        return cls(
            id=instance.id,
            city=instance.city,
            city_ascii=instance.city_ascii,
            country=instance.country,
            iso2=instance.iso2,
            iso3=instance.iso3,
            lat=instance.lat,
            lng=instance.lng,
            population=instance.population,
            use_on_app=instance.use_on_app,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "city_ascii": self.city_ascii,
            "country": self.country,
            "iso2": self.iso2,
            "iso3": self.iso3,
            "lat": self.lat,
            "lng": self.lng,
            "population": self.population,
            "use_on_app": self.use_on_app,
        }


class APIWorldCities(WorldCitiesContract):
    id: int


# APIWorldCitiesList contracts
class APIWorldCitiesList(BaseModel):
    """API World Cities List contract."""

    items: List[APIWorldCities]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django WorldCities queryset to APIWorldCities instances.
        """
        return cls(items=[APIWorldCities.from_model(i) for i in qs])


class WorldCitiesActiveContract(BaseModel):
    """World Cities Active contract."""

    city: str
    country: str

    @classmethod
    def from_model(cls, instance: WorldCitiesORM):
        """
        Convert a Django WorldCities model instance to an APIWorldCities instance.
        """
        return cls(
            city=instance.city,
            country=instance.country,
        )

    def to_dict(self):
        return {
            "city": self.city,
            "country": self.country,
        }


class APIWorldCitiesActiveList(BaseModel):
    """API World Cities Active List contract."""

    items: List[WorldCitiesActiveContract]

    @classmethod
    def from_qs(cls, qs):
        """
        Convert a Django WorldCities queryset to APIWorldCities instances.
        """
        return cls(items=[WorldCitiesActiveContract.from_model(i) for i in qs])

    def to_dict(self):
        return {
            "items": [i.to_dict() for i in self.items],
        }
