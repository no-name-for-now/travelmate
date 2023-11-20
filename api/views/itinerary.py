from typing import List

from django.db.models.query import QuerySet
from fastapi import Depends
from starlette.responses import JSONResponse

from api.models.itinerary import APIItineraryList
from api.models.itinerary import ItineraryORM
from api.models.itinerary_items import APIItineraryItemsList
from api.models.top_searched import APITopSearchedList
from api.models.unique_search_history import UniqueSearchHistoryORM
from api.utils.itinerary import get_itinerary__db
from api.utils.itinerary import get_itinerary__oai
from api.utils.itinerary import get_itinerary_items__oai
from api.utils.itinerary import get_top_n_itinerary


def itinerary_item_get__oai(
    itinerary_items: List = Depends(get_itinerary_items__oai),
) -> APIItineraryItemsList | JSONResponse:
    """
    Get city climate.
    """
    return (
        APIItineraryItemsList.from_qs(itinerary_items)
        if isinstance(itinerary_items, list)
        else itinerary_items
    )


def itinerary_get__oai(
    itinerary: List = Depends(get_itinerary__oai),
) -> APIItineraryList | JSONResponse:
    """
    Get itinerary from OpenAI.
    """
    return (
        APIItineraryList.from_qs(itinerary)
        if isinstance(itinerary, list)
        else itinerary
    )


def itinerary_get(
    itinerary: ItineraryORM = Depends(get_itinerary__db),
) -> APIItineraryList | JSONResponse:
    """
    Get itinerary from DB.
    """
    return (
        APIItineraryList.from_qs(itinerary)
        if itinerary.__class__ is QuerySet
        else itinerary
    )


def itinerary_get_top_n(
    top_itineraries: UniqueSearchHistoryORM = Depends(get_top_n_itinerary),
) -> APITopSearchedList | JSONResponse:
    """
    Get top {count} itineraries.
    """
    return (
        APITopSearchedList.from_qs(top_itineraries)
        if top_itineraries.__class__ is QuerySet
        else top_itineraries
    )
