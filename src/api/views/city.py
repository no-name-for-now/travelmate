from api.models.city_climate import APICityClimateList
from api.models.city_climate import CityClimateORM
from api.models.city_descriptors import APICityDescriptorsList
from api.models.city_descriptors import CityDescriptorsORM
from api.utils.city import get_city_climate__db
from api.utils.city import get_city_climate__oai
from api.utils.city import get_city_description__db
from api.utils.city import get_city_description__oai
from fastapi import Depends


def city_description_get__oai(
    city_descriptor: CityDescriptorsORM = Depends(get_city_description__oai),
) -> APICityDescriptorsList:
    """
    Get city description.
    """
    return (
        APICityDescriptorsList.from_qs(city_descriptor)
        if isinstance(city_descriptor, CityDescriptorsORM)
        else city_descriptor
    )


def city_description_get(
    city_descriptor: CityDescriptorsORM = Depends(get_city_description__db),
) -> APICityDescriptorsList:
    """
    Get city description.
    """
    return (
        APICityDescriptorsList.from_qs(city_descriptor)
        if isinstance(city_descriptor, CityDescriptorsORM)
        else city_descriptor
    )


def city_climate_get(
    city_climate: CityClimateORM = Depends(get_city_climate__db),
) -> APICityClimateList:
    """
    Get city climate.
    """
    return (
        APICityClimateList.from_qs(city_climate)
        if isinstance(city_climate, CityClimateORM)
        else city_climate
    )


def city_climate_get__oai(
    city_climate: CityClimateORM = Depends(get_city_climate__oai),
) -> APICityClimateList:
    """
    Get city climate.
    """
    return (
        APICityClimateList.from_qs(city_climate)
        if isinstance(city_climate, CityClimateORM)
        else city_climate
    )
