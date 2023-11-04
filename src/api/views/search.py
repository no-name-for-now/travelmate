from api.models.user_saved_itinerary import APIUserSavedItinerary
from api.models.user_saved_itinerary import UserSavedItineraryORM
from api.models.user_search import APIUserSearchList
from api.utils.search import get_user_search_history
from api.utils.search import post_user_search_history
from django.db.models.query import QuerySet
from fastapi import Depends
from starlette.responses import JSONResponse


def search_get(
    user_search: UserSavedItineraryORM = Depends(get_user_search_history),
) -> APIUserSearchList | JSONResponse:
    """
    Get a user's itinerary search history.
    """
    return (
        APIUserSearchList.from_qs(user_search)
        if user_search.__class__ is QuerySet
        else user_search
    )


def search_post(
    user_saved_itinerary: UserSavedItineraryORM = Depends(post_user_search_history),
) -> APIUserSavedItinerary | JSONResponse:
    """
    Store a user's search history.
    """
    return (
        APIUserSavedItinerary.from_model(user_saved_itinerary)
        if user_saved_itinerary.__class__ is QuerySet
        else user_saved_itinerary
    )
