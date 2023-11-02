from api.models import APIUserSavedItinerary
from api.models import APIUserSearchList
from api.models import UserSavedItineraryContract
from api.models import UserSavedItineraryORM
from api.models import UserSearchContract
from api.utils import get_unique_search_history
from api.utils import get_user_search_history
from fastapi import Depends


"""
UserItinerary
"""


def search_get(
    user_search: UserSearchContract = Depends(get_user_search_history),
) -> APIUserSearchList:
    """
    Get a user's itinerary search history.
    """
    # TODO: handle empty response
    return APIUserSearchList.from_qs(user_search)


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
