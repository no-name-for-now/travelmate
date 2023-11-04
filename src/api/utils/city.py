from api.models.city_descriptors import CityDescriptorsORM
from api.utils.base import get_object__oai
from api.utils.http import Error
from api.utils.validations import validate_get_city_description
from fastapi import Query


def get_city_description__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    # TODO: add in handling fetch from OpenAI and persist to DB, and return
    # Currently just returns from DB
    ok, _city, _country = validate_get_city_description(
        {"city": city, "country": country}
    )
    try:
        if ok:
            qs = get_object__oai(
                model_class=CityDescriptorsORM,
                class_function="get_city_description",
                city=_city,
                country=_country,
            )
            if not qs:
                return Error(404, "city entry not found", __name__)
            else:
                return qs
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e, __name__)


def get_city_description__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    ok, _city, _country = validate_get_city_description(
        {"city": city, "country": country}
    )

    try:
        if ok:
            qs = CityDescriptorsORM.objects.select_related("city").filter(
                city__city=_city, city__country=_country
            )
            if not qs:
                return Error(404, "city enrty not found", __name__)
            else:
                return qs
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e, __name__)
