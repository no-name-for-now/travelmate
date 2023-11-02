from fastapi import Depends

from api.models import UserSavedItineraryORM, UserSavedItineraryContract, APIUserSavedItinerary
from api.utils import get_unique_search_history


"""
UserItinerary
"""
def search_post(
    user_saved_itinerary: UserSavedItineraryContract,
    unique_search_history = Depends(get_unique_search_history)
) -> APIUserSavedItinerary:
    """
    Store a user's search history.
    """
    usi = UserSavedItineraryORM.from_api(unique_search_history, user_saved_itinerary)
    usi.save()
    return APIUserSavedItinerary.from_model(usi)
