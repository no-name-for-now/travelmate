from django.db import models
from fastapi import Body
from fastapi import Query

from api.models.unique_search_history import UniqueSearchHistoryORM
from api.models.user_saved_itinerary import UserSavedItineraryContract
from api.models.user_saved_itinerary import UserSavedItineraryORM
from api.utils.base import get_object_by_id
from api.utils.http import Error
from api.utils.validations import validate_store_user_search


def get_unique_search_history(
    unique_search_history_id: str = Query(
        ..., description="The ID of the unique search history."
    )
) -> models.Model:
    """Retrieve a unique search history by ID."""
    try:
        qs = get_object_by_id(UniqueSearchHistoryORM, unique_search_history_id)
        if not qs:
            return Error(404, "unique search history not found", __name__)
        else:
            return qs
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def get_user_search_history(
    user_id: str = Query(..., description="The ID of the user.")
) -> models.Model:
    """Retrieve a user's search history by ID."""
    try:
        qs = UserSavedItineraryORM.objects.select_related(
            "unique_search_history"
        ).filter(user_id=user_id)
        if not qs:
            return Error(404, "itinerary not found", __name__)
        else:
            return qs
    except Exception as e:
        return Error(500, e.__str__(), __name__)


def post_user_search_history(
    data: UserSavedItineraryContract = Body(
        ..., description="The user's search parameters."
    ),
) -> models.Model:
    """Store a user's search history."""
    ok = validate_store_user_search(data)
    try:
        if ok:
            obj = UserSavedItineraryORM.from_api(data)
            obj.save()
            return obj
        else:
            return Error(422, "invalid body", __name__)
    except Exception as e:
        return Error(500, e.__str__(), __name__)
