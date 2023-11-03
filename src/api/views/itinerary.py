from api.models.itinerary import APIItineraryList
from api.models.itinerary import ItineraryORM
from api.utils.itinerary import get_itinerary__db
from api.utils.itinerary import get_itinerary__oai
from fastapi import Depends


def itinerary_get__oai(
    itinerary: ItineraryORM = Depends(get_itinerary__oai),
) -> APIItineraryList:
    """
    Get itinerary from OpenAI.
    """
    return APIItineraryList.from_qs(itinerary)


def itinerary_get(
    itinerary: ItineraryORM = Depends(get_itinerary__db),
) -> APIItineraryList:
    """
    Get itinerary from DB.
    """
    return APIItineraryList.from_qs(itinerary)
