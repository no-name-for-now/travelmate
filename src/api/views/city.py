from api.models.city_descriptors import APICityDescriptorsList
from api.models.city_descriptors import CityDescriptorsORM
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
