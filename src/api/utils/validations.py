cities_list = [
    {"country": "Belgium", "cities": "Antwerp"},
    {"country": "Belgium", "cities": "Brussels"},
    {"country": "Belgium", "cities": "Gent"},
    {"country": "Belgium", "cities": "Charleroi"},
    {"country": "Belgium", "cities": "Liege"},
    {"country": "Germany", "cities": "Berlin"},
    {"country": "Germany", "cities": "Stuttgart"},
    {"country": "Germany", "cities": "Munich"},
    {"country": "Spain", "cities": "Madrid"},
    {"country": "Spain", "cities": "Barcelona"},
    {"country": "Spain", "cities": "Sevilla"},
    {"country": "Spain", "cities": "Malaga"},
    {"country": "Portugal", "cities": "Aves"},
    {"country": "Portugal", "cities": "Sintra"},
    {"country": "Portugal", "cities": "Vila Nova de Gaia"},
    {"country": "Portugal", "cities": "Cascais"},
    {"country": "Portugal", "cities": "Lisbon"},
    {"country": "Portugal", "cities": "Porto"},
]


def validate_first_backend(itenerary_dict):
    """Validate the input for the first_backend endpoint."""
    location_request = {key: itenerary_dict[key] for key in ["cities", "country"]}
    if location_request not in cities_list:
        return False

    if itenerary_dict["days"] > 7:
        return False

    return True


def validate_get_city_description(itenerary_dict):
    """Validate the input for the get_city_description endpoint."""
    if itenerary_dict in cities_list:
        return True
    else:
        return False


def validate_store_user_search(itenerary_dict):
    """Validate the input for the store_user_search endpoint."""
    return True
