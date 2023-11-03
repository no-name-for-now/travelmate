from api.models.user_saved_itinerary import APIUserSavedItinerary
from api.models.user_search import APIUserSearchList
from api.views import search as views
from fastapi import APIRouter


router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses={404: {"description": "Not found"}},
)

router.get(
    "/user",
    summary="Get a user's itinerary search history.",
    response_model=APIUserSearchList,
    name="search-get",
)(views.search_get)

router.post(
    "/user",
    summary="Store a user's search history.",
    response_model=APIUserSavedItinerary,
    name="search-post",
)(views.search_post)
