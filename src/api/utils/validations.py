from typing import Any
from typing import Dict

cities_list = [
    {"country": "Belgium", "city": "Antwerp"},
    {"country": "Belgium", "city": "Brussels"},
    {"country": "Belgium", "city": "Gent"},
    {"country": "Belgium", "city": "Charleroi"},
    {"country": "Belgium", "city": "Liege"},
    {"country": "Germany", "city": "Berlin"},
    {"country": "Germany", "city": "Stuttgart"},
    {"country": "Germany", "city": "Munich"},
    {"country": "Spain", "city": "Madrid"},
    {"country": "Spain", "city": "Barcelona"},
    {"country": "Spain", "city": "Sevilla"},
    {"country": "Spain", "city": "Malaga"},
    {"country": "Portugal", "city": "Aves"},
    {"country": "Portugal", "city": "Sintra"},
    {"country": "Portugal", "city": "Vila Nova de Gaia"},
    {"country": "Portugal", "city": "Cascais"},
    {"country": "Portugal", "city": "Lisbon"},
    {"country": "Portugal", "city": "Porto"},
]


def validate_itinerary(itinerary_dict: Dict[str, Any]):
    """Validate the input for the itinerary endpoint."""
    if dict((k, itinerary_dict[k]) for k in ("country", "city")) in cities_list:
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
    if itinerary_dict in cities_list:
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
    return True
