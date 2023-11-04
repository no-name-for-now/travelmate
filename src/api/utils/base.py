from typing import Type

from django.db import models
from tripagenda import oai


def get_object_by_id(model_class: Type[models.Model], id: str) -> models.Model:
    """
    Retrieve an object by id.

    This is a generic helper method that will retrieve any object by ID.
    """
    return model_class.objects.get(pk=id)


def get_object__oai(
    model_class: Type[models.Model],
    class_function: str,
    **kwargs,
) -> models.Model:
    """
    Get queryset from openai response.

    Parameters
    ----------
    model_class : Type[models.Model]
        the model class to return
    class_function : str
        the function to call on the oai module
    kwargs : dict
        the kwargs to pass to the function

    Returns
    -------
    - queryset of model_class

    """
    function = getattr(oai, class_function)
    res = function(kwargs)

    obj = model_class.from_api(res)
    obj.save()

    return obj
