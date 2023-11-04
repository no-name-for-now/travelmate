from api.models.itinerary import ItineraryORM
from api.models.unique_search_history import UniqueSearchHistoryORM
from api.utils.http import Error
from api.utils.validations import validate_itinerary
from django.db.models import Count
from fastapi import Path
from fastapi import Query
from fastapi.responses import JSONResponse


def get_itinerary__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
    days: int = Query(..., description="The number of days to spend in the city."),
) -> ItineraryORM | JSONResponse:
    """Retrieve an itinerary from OpenAI."""
    ok, _city, _country, _days = validate_itinerary(
        {"city": city, "country": country, "days": days}
    )

    try:
        if ok:
            qs = ItineraryORM.objects.select_related("unique_search_history").filter(
                unique_search_history__city=_city,
                unique_search_history__country=_country,
                unique_search_history__num_days=_days,
            )
            if not qs:
                return Error(404, "itinerary not found", __name__)
            return qs
        else:
            return Error(422, "invalid number of days, city or country", __name__)
    except Exception as e:
        return Error(500, e, __name__)


def get_itinerary__db(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
    days: int = Query(..., description="The number of days to spend in the city."),
) -> ItineraryORM:
    """Retrieve an itinerary from the database."""
    ok, _city, _country, _days = validate_itinerary(
        {"city": city, "country": country, "days": days}
    )

    try:
        if ok:
            qs = ItineraryORM.objects.select_related("unique_search_history").filter(
                unique_search_history__city=_city,
                unique_search_history__country=_country,
                unique_search_history__num_days=_days,
            )
            if not qs:
                return Error(404, "itinerary not found", __name__)
            return qs
        else:
            return Error(422, "invalid number of days, city or country", __name__)
    except Exception as e:
        return Error(500, e, __name__)


def get_top_n_itinerary(
    count: int = Path(..., description="The number of itineraries to retrieve."),
) -> UniqueSearchHistoryORM:
    """Retrieve the top {count} itineraries from the database."""
    try:
        qs = (
            UniqueSearchHistoryORM.objects.annotate(
                number_of_searches=Count("searchhistoryorm")
            )
            .values("country", "city", "num_days", "number_of_searches")
            .order_by("-number_of_searches")[:count]
        )
        if not qs:
            return Error(404, "itinerary not found", __name__)
        return qs
    except Exception as e:
        return Error(500, e, __name__)
