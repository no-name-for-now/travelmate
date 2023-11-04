from typing import Any
from typing import Dict

from api.models.world_cities import APIWorldCitiesActiveList
from api.models.world_cities import WorldCitiesORM


cities_list = APIWorldCitiesActiveList.from_qs(
    WorldCitiesORM.objects.filter(use_on_app=True).all()
)
active_citiies = cities_list.items


def validate_itinerary(itinerary_dict: Dict[str, Any]):
    """Validate the input for the itinerary endpoint."""
    if dict((k, itinerary_dict[k]) for k in ("country", "city")) in active_citiies:
        days = itinerary_dict["days"]

        if days > 0 and days <= 7:
            city = itinerary_dict["city"].strip()
            country = itinerary_dict["country"].strip()

            if city == "" or country == "":
                return False, None, None, None

            return True, city, country, days
        else:
            return False, None, None, None

    return False, None, None, None


def validate_get_city(itinerary_dict):
    """Validate the input for the get_city_description endpoint."""
    if itinerary_dict in active_citiies:
        city = itinerary_dict["city"].strip()
        country = itinerary_dict["country"].strip()
        if city == "" or country == "":
            return False, None, None
        else:
            return True, city, country
    else:
        return False, None, None


def validate_store_user_search(itenerary_dict):
    """Validate the input for the store_user_search endpoint."""
    _ = itenerary_dict
    return True
