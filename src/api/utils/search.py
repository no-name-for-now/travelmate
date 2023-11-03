from api.models.unique_search_history import UniqueSearchHistoryORM
from api.models.user_saved_itinerary import UserSavedItineraryORM
from api.utils.base import get_object_by_id
from django.db import models
from fastapi import Query


def get_unique_search_history(
    ush_id: str = Query(..., description="The ID of the unique search history.")
) -> models.Model:
    """Retrieve a unique search history by ID."""
    return get_object_by_id(UniqueSearchHistoryORM, ush_id)


def get_user_search_history(
    user_id: str = Query(..., description="The ID of the user.")
) -> models.Model:
    """Retrieve a user's search history by ID."""
    return UserSavedItineraryORM.objects.select_related("ush").filter(user_id=user_id)
