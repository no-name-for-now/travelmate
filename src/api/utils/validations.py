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


def validate_first_backend(itenerary_dict):
    """Validate the input for the first_backend endpoint."""
    location_request = {key: itenerary_dict[key] for key in ["city", "country"]}
    if location_request not in cities_list:
        return False

    if itenerary_dict["days"] > 7:
        return False

    return True


def validate_get_city_description(itinerary_dict):
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
