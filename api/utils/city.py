from typing import List

from fastapi import Query
from starlette.responses import JSONResponse

from api.models.city_climate import CityClimateORM
from api.models.city_descriptors import CityDescriptorsORM
from api.models.itinerary_items import ItineraryItemsORM
from api.models.world_cities import WorldCitiesORM
from api.utils.base import get_object__oai
from api.utils.base import oai_obj_to_qs
from api.utils.http import Error
from api.utils.validations import validate_get_city
from tripagenda import logger


def get_city_description__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})
    try:
        if ok:
            res = get_object__oai(
                class_function="get_city_description",
                city=_city,
                country=_country,
            )

            qs = oai_obj_to_qs(CityDescriptorsORM, res)
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


def get_city_item__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> List | JSONResponse:
    """Retrieve a city's climate by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            res = get_object__oai(
                class_function="get_city_items",
                city=_city,
                country=_country,
            )
            logger.info(res)
            res = res["itinerary"]
            logger.info(res)

            obj = oai_obj_to_qs(ItineraryItemsORM, res)
            logger.info("trying to load data, should break")
            if not obj:
                return Error(404, "city entry not found", __name__)
            else:
                return obj
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def get_city_climate__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> List | JSONResponse:
    """Retrieve a city's climate by city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            res = get_object__oai(
                class_function="get_city_climate",
                city=_city,
                country=_country,
            )

            monthly_data = list()
            for month, low, high, rain in zip(
                res["month"], res["low"], res["high"], res["rainfall"]
            ):
                monthly_data.append(
                    {
                        "city": city,
                        "month": month,
                        "low": low,
                        "high": high,
                        "rainfall": rain,
                    }
                )

            obj = oai_obj_to_qs(CityClimateORM, monthly_data)
            if not obj:
                return Error(404, "city entry not found", __name__)
            else:
                return obj
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
