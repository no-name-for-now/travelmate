from api.models.city_descriptors import CityDescriptorsORM
from django.db import models
from fastapi import Query


def get_city_description__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> models.Model:
    """Retrieve a city description by city and country."""
    #  TODO: add validation
    #  TODO: add in coroutines for handling empty descriptions
    # if description from DB is empty, hit OpenAI API
    # format data response, return to requestet
    # at the same time, persist results to DB
    return CityDescriptorsORM.objects.get(city=city, country=country)


def get_city_description__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> models.Model:
    """Retrieve a city description by city and country."""
    return CityDescriptorsORM.objects.get(city=city, country=country)
