from api.models.itinerary import ItineraryORM
from api.utils.validations import validate_itinerary
from fastapi import HTTPException
from fastapi import Query


def get_itinerary__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
    days: int = Query(..., description="The number of days to spend in the city."),
) -> ItineraryORM:
    """Retrieve an itinerary from OpenAI."""
    ok, _city, _country, _days = validate_itinerary(
        {"city": city, "country": country, "days": days}
    )
    if ok:
        return ItineraryORM.objects.select_related("unique_search_history").filter(
            unique_search_history__city=_city,
            unique_search_history__country=_country,
            unique_search_history__num_days=_days,
        )
    else:
        raise HTTPException(
            status_code=422,
            detail="Unprocessable entity - invalid number of days, city or country.",
        )


def get_itinerary__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
    days: int = Query(..., description="The number of days to spend in the city."),
) -> ItineraryORM:
    """Retrieve an itinerary from the database."""
    ok, _city, _country, _days = validate_itinerary(
        {"city": city, "country": country, "days": days}
    )

    if ok:
        return ItineraryORM.objects.select_related("unique_search_history").filter(
            unique_search_history__city=_city,
            unique_search_history__country=_country,
            unique_search_history__num_days=_days,
        )
    else:
        raise HTTPException(
            status_code=422,
            detail="Unprocessable entity - invalid number of days, city or country.",
        )
