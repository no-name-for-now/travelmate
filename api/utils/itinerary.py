from typing import List

from django.db.models import Count
from fastapi import Path
from fastapi import Query
from fastapi.responses import JSONResponse

from api.models.itinerary import ItineraryORM
from api.models.itinerary_items import ItineraryItemsORM
from api.models.unique_search_history import UniqueSearchHistoryORM
from api.utils.base import get_object__oai
from api.utils.base import oai_obj_to_qs
from api.utils.http import Error
from api.utils.validations import validate_get_city
from api.utils.validations import validate_itinerary


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
            unique_search_history = UniqueSearchHistoryORM.objects.filter(
                city=_city,
                country=_country,
                num_days=_days,
            ).first()

            if unique_search_history:
                return get_itinerary__db(city, country, days)
            else:
                # create a new unique search history
                unique_search_history = UniqueSearchHistoryORM.from_api(
                    {
                        "city": _city,
                        "country": _country,
                        "num_days": _days,
                    }
                )
                unique_search_history.save()

                unique_search_history_id = unique_search_history.id

                res = get_object__oai(
                    class_function="get_itinerary",
                    city=_city,
                    country=_country,
                    num_days=_days,
                )

                activities = list()
                for activity in res["activities"]:
                    activities.append(
                        {
                            "unique_search_history_id": unique_search_history_id,
                            "day": activity["day"],
                            "city": activity["city"],
                            "travel_method": activity["travel_method"],
                            "travel_time": activity["travel_time"],
                            "morning_activity": activity["morning_activity"],
                            "afternoon_activity": activity["afternoon_activity"],
                            "evening_activity": activity["evening_activity"],
                        }
                    )

                if not activities:
                    return Error(404, "itinerary not found", __name__)
                else:
                    obj = oai_obj_to_qs(ItineraryORM, activities)
                    if not obj:
                        return Error(404, "itinerary not found", __name__)
                    else:
                        return obj
        else:
            return Error(422, "invalid number of days, city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)


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
        return Error(500, e.__str__(), __name__)


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
        return Error(500, e.__str__(), __name__)


def get_itinerary_items__oai(
    city: str = Query(..., description="The name of the city."),
    country: str = Query(..., description="The name of the country."),
) -> List | JSONResponse:
    """Retrieve itinerary items for city and country."""
    ok, _city, _country = validate_get_city({"city": city, "country": country})

    try:
        if ok:
            res = get_object__oai(
                class_function="get_itinerary_items",
                city=_city,
                country=_country,
            )
            res = res["itinerary"]
            for i in res:
                i["city"] = city

            obj = oai_obj_to_qs(ItineraryItemsORM, res)
            if not obj:
                return Error(404, "city entry not found", __name__)
            else:
                return obj
        else:
            return Error(422, "invalid city or country", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)
