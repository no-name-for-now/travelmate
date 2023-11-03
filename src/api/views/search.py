from api.models.user_saved_itinerary import APIUserSavedItinerary
from api.models.user_saved_itinerary import UserSavedItineraryContract
from api.models.user_saved_itinerary import UserSavedItineraryORM
from api.models.user_search import APIUserSearchList
from api.utils.search import get_user_search_history
from fastapi import Depends


def search_get(
    user_search=Depends(get_user_search_history),
) -> APIUserSearchList:
    """
    Get a user's itinerary search history.
    """
    # TODO: handle empty response
    return APIUserSearchList.from_qs(user_search)


def search_post(
    user_saved_itinerary: UserSavedItineraryContract,
) -> APIUserSavedItinerary:
    """
    Store a user's search history.
    """
    # TODO: should handle updates if record exists?
    # Option to add a searc_put view here
    usi = UserSavedItineraryORM.from_api(user_saved_itinerary)
    usi.save()
    return APIUserSavedItinerary.from_model(usi)
