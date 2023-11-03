from api.models.city_descriptors import CityDescriptorsORM
from api.utils.validations import validate_get_city_description
from fastapi import HTTPException
from fastapi import Query
from tripagenda import logger


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
    if ok:
        return CityDescriptorsORM.objects.select_related("city").filter(
            city__city=_city, city__country=_country
        )
    else:
        raise HTTPException(
            status_code=422, detail="Unprocessable entity - invalid city or country."
        )


def get_city_description__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> CityDescriptorsORM:
    """Retrieve a city description by city and country."""
    ok, _city, _country = validate_get_city_description(
        {"city": city, "country": country}
    )
    logger.info(f"get_city_description__db: ok={ok}, city={_city}, country={_country}")
    if ok:
        return CityDescriptorsORM.objects.select_related("city").filter(
            city__city=_city, city__country=_country
        )
    else:
        raise HTTPException(
            status_code=422, detail="Unprocessable entity - invalid city or country."
        )
