from api.models.user_saved_itinerary import APIUserSavedItinerary
from api.models.user_search import APIUserSearchList
from api.utils.http import responses
from api.views import search as views
from fastapi import APIRouter
from fastapi import status


router = APIRouter(
    prefix="/search",
    tags=["search"],
    responses=responses,
)

router.get(
    "/user",
    summary="Get a user's itinerary search history.",
    response_model=APIUserSearchList,
    name="search-get",
    status_code=status.HTTP_200_OK,
)(views.search_get)

router.post(
    "/user",
    summary="Store a user's search history.",
    response_model=APIUserSavedItinerary,
    name="search-post",
    status_code=status.HTTP_201_CREATED,
)(views.search_post)
