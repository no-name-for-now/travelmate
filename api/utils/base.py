from typing import Any
from typing import Type

from django.db import models

from tripagenda import logger
from tripagenda import oai


def get_object_by_id(model_class: Type[models.Model], id: str) -> models.Model:
    """
    Retrieve an object by id.

    This is a generic helper method that will retrieve any object by ID.
    """
    return model_class.objects.get(pk=id)


def get_object__oai(
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
    - OpenAI Reponse : dict

    """
    try:
        function = getattr(oai, class_function)
        res = function(**kwargs)

        if res.get("error", False):
            logger.error(res["error_message"])
            raise Exception(res["error_message"])

        return res
    except Exception as e:
        logger.error(e)
        raise e


def oai_obj_to_qs(model_class: Type[models.Model], oai_obj: Any) -> models.Model:
    """
    Convert an oai object to a queryset.

    Parameters
    ----------
    model_class : Type[models.Model]
        the model class to return
    oai_obj : dict
        the oai object to convert

    Returns
    -------
    - queryset of model_class

    """
    # try:
    if isinstance(oai_obj, dict):
        obj = model_class.from_oai(oai_model=oai_obj)
        logger.info(obj)
        obj.save()
    elif isinstance(oai_obj, list):
        obj = model_class.objects.bulk_create(
            [model_class.from_oai(oai_model=o) for o in oai_obj]
        )
    else:
        raise Exception("oai_obj must be a dict or list")

    return obj
    # except Exception as e:
    #    logger.error(e)
    #    raise e
