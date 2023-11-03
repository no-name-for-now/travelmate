from api.models.user_search import APIUserSearchList
from api.views import city as views
from fastapi import APIRouter


router = APIRouter(
    prefix="/city",
    tags=["city"],
    responses={404: {"description": "Not found"}},
)

router.get(
    "/description",
    summary="Get city description.",
    response_model=APIUserSearchList,
    name="city-description-get",
)(views.city_description_get)

router.get(
    "/description/oai",
    summary="Get city description from OpenAI.",
    response_model=APIUserSearchList,
    name="city-description-get-oai",
)(views.city_description_get__oai)
