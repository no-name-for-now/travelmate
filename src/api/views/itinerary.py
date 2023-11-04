from api.models.itinerary import APIItineraryList
from api.models.itinerary import ItineraryORM
from api.models.top_searched import APITopSearchedList
from api.models.unique_search_history import UniqueSearchHistoryORM
from api.utils.itinerary import get_itinerary__db
from api.utils.itinerary import get_itinerary__oai
from api.utils.itinerary import get_top_n_itinerary
from fastapi import Depends
from fastapi.responses import JSONResponse
from tripagenda import logger


def itinerary_get__oai(
    itinerary: ItineraryORM = Depends(get_itinerary__oai),
) -> APIItineraryList:
    """
    Get itinerary from OpenAI.
    """
    return APIItineraryList.from_qs(itinerary)


def itinerary_get(
    itinerary: ItineraryORM | JSONResponse = Depends(get_itinerary__db),
) -> APIItineraryList:
    """
    Get itinerary from DB.
    """
    res = (
        APIItineraryList.from_qs(itinerary)
        if isinstance(itinerary, ItineraryORM)
        else itinerary
    )
    logger.info(f"itinerary_get: {res}")
    return res


def itinerary_get_top_n(
    top_itineraries: UniqueSearchHistoryORM = Depends(get_top_n_itinerary),
) -> APITopSearchedList:
    """
    Get top {count} itineraries.
    """
    return APITopSearchedList.from_qs(top_itineraries)
