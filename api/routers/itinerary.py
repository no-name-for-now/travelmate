from fastapi import APIRouter
from fastapi import status

from api.models.itinerary import APIItineraryList
from api.models.itinerary_items import APIItineraryItemsList
from api.models.top_searched import APITopSearchedList
from api.utils.http import responses
from api.views import itinerary as views


router = APIRouter(
    prefix="/itinerary",
    tags=["itinerary"],
    responses=responses,
)

router.get(
    "/",
    summary="Get itinerary.",
    response_model=APIItineraryList,
    name="itinerary-get",
    status_code=status.HTTP_200_OK,
)(views.itinerary_get)

router.get(
    "/oai",
    summary="Get itinerary from OpenAI.",
    response_model=APIItineraryList,
    name="itinerary-get-oai",
    status_code=status.HTTP_200_OK,
)(views.itinerary_get__oai)

router.get(
    "/top/{count}",
    summary="Get top {count} itineraries.",
    response_model=APITopSearchedList,
    name="itinerary-get-top-n",
    status_code=status.HTTP_200_OK,
)(views.itinerary_get_top_n)

router.get(
    "/items/oai",
    summary="Get itinerary items from OpenAI.",
    response_model=APIItineraryItemsList,
    name="city-items-get-oai",
    status_code=status.HTTP_200_OK,
)(views.itinerary_item_get__oai)
