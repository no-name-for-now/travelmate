from typing import Type

from django.db import models
from fastapi import HTTPException


def get_object_by_id(model_class: Type[models.Model], id: str) -> models.Model:
    """
    Retrieve an object by id.

    This is a generic helper method that will retrieve any object by ID.
    """
    instance = model_class.objects.get(pk=id)
    if not instance:
        raise HTTPException(status_code=404, detail="Object not found.")
    return instance
