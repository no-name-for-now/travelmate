from typing import List

from django.db.models.query import QuerySet
from fastapi import Depends
from starlette.responses import JSONResponse

from api.models.city_climate import APICityClimateList
from api.models.city_climate import CityClimateORM
from api.models.city_cost_of_living import APICityCostOfLivingList
from api.models.city_descriptors import APICityDescriptorsList
from api.models.city_descriptors import CityDescriptorsContract
from api.models.city_descriptors import CityDescriptorsORM
from api.models.world_cities import APIWorldCitiesActiveList
from api.models.world_cities import WorldCitiesORM
from api.utils.city import get_cities_active__db
from api.utils.city import get_cities_cost_of_living__numbeo
from api.utils.city import get_city_climate__db
from api.utils.city import get_city_climate__oai
from api.utils.city import get_city_description__db
from api.utils.city import get_city_description__oai


def city_description_get__oai(
    city_descriptor: CityDescriptorsORM = Depends(get_city_description__oai),
) -> CityDescriptorsContract | JSONResponse:
    """
    Get city description.
    """
    return (
        CityDescriptorsContract.from_model(city_descriptor)
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
    city_climate: List = Depends(get_city_climate__oai),
) -> APICityClimateList | JSONResponse:
    """
    Get city climate.
    """
    return (
        APICityClimateList.from_qs(city_climate)
        if isinstance(city_climate, list)
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


def cities_cost_of_living_get(
    cost_of_living: List = Depends(get_cities_cost_of_living__numbeo),
) -> APICityCostOfLivingList | JSONResponse:
    """
    Get cities cost of living.
    """
    return (
        APICityCostOfLivingList.from_qs(cost_of_living)
        if isinstance(cost_of_living, list)
        else cost_of_living
    )
