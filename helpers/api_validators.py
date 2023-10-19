
cities_list = [
  { "country": "Belgium", "cities": "Antwerp" },
  { "country": "Belgium", "cities": "Brussels" },
  { "country": "Spain", "cities": "Madrid" },
  { "country": "Portugal", "cities": "Lisbon" },
  { "country": "Portugal", "cities": "Porto" }
]






def validate_first_backend(itenerary_dict):
	location_request = {key:itenerary_dict[key] for key in ['cities','country']}
	if location_request not in cities_list:
		return False

	if (itenerary_dict['to_date_obj'] - itenerary_dict['from_date_obj']).days > 7:
		return False
	
	return True


def validate_get_city_description(itenerary_dict):
	if itenerary_dict in cities_list:
		return True
	else:
		return False

	