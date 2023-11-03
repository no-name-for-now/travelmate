from api.models.city_descriptors import APICityDescriptors
from api.models.city_descriptors import CityDescriptorsContract
from api.utils.city import get_city_description__db
from api.utils.city import get_city_description__oai
from fastapi import Depends


def city_description_get__oai(
    city_descriptor: CityDescriptorsContract = Depends(get_city_description__oai),
) -> APICityDescriptors:
    """
    Get city description.
    """
    return APICityDescriptors.from_model(city_descriptor)


def city_description_get(
    city_descriptor: CityDescriptorsContract = Depends(get_city_description__db),
) -> APICityDescriptors:
    """
    Get city description.
    """
    return APICityDescriptors.from_model(city_descriptor)
