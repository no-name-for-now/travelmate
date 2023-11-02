from api.models import APIUserSavedItinerary
from api.models import UserSavedItineraryContract
from api.models import UserSavedItineraryORM
from api.utils import get_unique_search_history
from fastapi import Depends


"""
UserItinerary
"""


def search_post(
    user_saved_itinerary: UserSavedItineraryContract,
    unique_search_history=Depends(get_unique_search_history),
) -> APIUserSavedItinerary:
    """
    Store a user's search history.
    """
    usi = UserSavedItineraryORM.from_api(unique_search_history, user_saved_itinerary)
    usi.save()
    return APIUserSavedItinerary.from_model(usi)
