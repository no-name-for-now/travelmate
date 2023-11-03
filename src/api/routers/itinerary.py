from api.models.itinerary import APIItineraryList
from api.views import itinerary as views
from fastapi import APIRouter


router = APIRouter(
    prefix="/itinerary",
    tags=["itinerary"],
    responses={404: {"description": "Not found"}},
)

router.get(
    "/",
    summary="Get itinerary.",
    response_model=APIItineraryList,
    name="itinerary-get",
)(views.itinerary_get)

router.get(
    "/oai",
    summary="Get itinerary from OpenAI.",
    response_model=APIItineraryList,
    name="itinerary-get-oai",
)(views.itinerary_get__oai)
