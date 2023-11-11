from fastapi import Query

from api.models.city_climate import CityClimateORM
from api.models.city_descriptors import CityDescriptorsORM
from api.models.world_cities import WorldCitiesORM
from api.utils.base import get_object__oai
from api.utils.http import Error
from api.utils.validations import validate_get_city


def get_city_description__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    # TODO: add in handling fetch from OpenAI and persist to DB, and return
    # Currently just returns from DB
    ok, _city, _country = validate_get_city({"city": city, "country": country})
    try:
        if ok:
            qs = get_object__oai(
                model_class=CityDescriptorsORM,
                class_function="get_city_description",
                city=_city,
                country=_country,
            ).first()
            if not qs:
                return Error(404, "city entry not found", __name__)
            else:
                return qs
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def get_city_description__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            qs = (
                CityDescriptorsORM.objects.select_related("city")
                .filter(city__city=_city, city__country=_country)
                .first()
            )
            if not qs:
                return Error(404, "city entry not found", __name__)
            else:
                return qs
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def get_city_climate__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityClimateORM:
    """Retrieve a city's climate by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            qs = get_object__oai(
                model_class=CityClimateORM,
                class_function="get_city_climate",
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
        return Error(500, e.__str__(), __name__)


def get_city_climate__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityClimateORM:
    """Retrieve a city's climate by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            qs = CityClimateORM.objects.select_related("city").filter(
                city__city=_city, city__country=_country
            )
            if not qs:
                return Error(404, "city entry not found", __name__)
            else:
                return qs
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def get_cities_active__db() -> WorldCitiesORM:
    """Retrieve all active cities."""
    try:
        qs = WorldCitiesORM.objects.filter(use_on_app=True)
        if not qs:
            return Error(404, "no active cities found", __name__)
        else:
            return qs
    except Exception as e:
        return Error(500, e.__str__(), __name__)
