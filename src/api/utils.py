"""Utility functions for the API."""
from typing import Type

from api.models import UniqueSearchHistoryORM
from django.db import models
from fastapi import HTTPException
from fastapi import Query


def get_object(model_class: Type[models.Model], id: str) -> models.Model:
    """
    Retrieve an object by id.

    This is a generic helper method that will retrieve any object by ID.
    """
    instance = model_class.objects.filter(pk=id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance


def get_unique_search_history(
    ush_id: str = Query(..., description="The ID of the unique search history.")
) -> models.Model:
    """Retrieve a unique search history by ID."""
    return get_object(UniqueSearchHistoryORM, ush_id)
