from api.models.city_climate import APICityClimateList
from api.models.city_climate import CityClimateORM
from api.models.city_descriptors import APICityDescriptorsList
from api.models.city_descriptors import CityDescriptorsORM
from api.models.world_cities import APIWorldCitiesActiveList
from api.models.world_cities import WorldCitiesORM
from api.utils.city import get_cities_active__db
from api.utils.city import get_city_climate__db
from api.utils.city import get_city_climate__oai
from api.utils.city import get_city_description__db
from api.utils.city import get_city_description__oai
from django.db.models.query import QuerySet
from fastapi import Depends
from starlette.responses import JSONResponse


def city_description_get__oai(
    city_descriptor: CityDescriptorsORM = Depends(get_city_description__oai),
) -> APICityDescriptorsList | JSONResponse:
    """
    Get city description.
    """
    return (
        APICityDescriptorsList.from_qs(city_descriptor)
        if city_descriptor.__class__ is QuerySet
        else city_descriptor
    )


def city_description_get(
    city_descriptor: CityDescriptorsORM = Depends(get_city_description__db),
) -> APICityDescriptorsList | JSONResponse:
    """
    Get city description.
    """
    return (
        APICityDescriptorsList.from_qs(city_descriptor)
        if city_descriptor.__class__ is QuerySet
        else city_descriptor
    )


def city_climate_get(
    city_climate: CityClimateORM = Depends(get_city_climate__db),
) -> APICityClimateList | JSONResponse:
    """
    Get city climate.
    """
    return (
        APICityClimateList.from_qs(city_climate)
        if city_climate.__class__ is QuerySet
        else city_climate
    )


def city_climate_get__oai(
    city_climate: CityClimateORM = Depends(get_city_climate__oai),
) -> APICityClimateList | JSONResponse:
    """
    Get city climate.
    """
    return (
        APICityClimateList.from_qs(city_climate)
        if city_climate.__class__ is QuerySet
        else city_climate
    )


def cities_active_get(
    cities: WorldCitiesORM = Depends(get_cities_active__db),
) -> APIWorldCitiesActiveList | JSONResponse:
    """
    Get all active cities.
    """
    return (
        APIWorldCitiesActiveList.from_qs(cities)
        if cities.__class__ is QuerySet
        else cities
    )
