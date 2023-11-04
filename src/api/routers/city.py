from api.models.city_climate import APICityClimateList
from api.models.city_descriptors import APICityDescriptorsList
from api.views import city as views
from fastapi import APIRouter
from fastapi import status
from tripagenda.routers import responses


router = APIRouter(
    prefix="/city",
    tags=["city"],
    responses=responses,
)

router.get(
    "/description",
    summary="Get city description.",
    response_model=APICityDescriptorsList,
    name="city-description-get",
    status_code=status.HTTP_200_OK,
)(views.city_description_get)

router.get(
    "/description/oai",
    summary="Get city description from OpenAI.",
    response_model=APICityDescriptorsList,
    name="city-description-get-oai",
    status_code=status.HTTP_200_OK,
)(views.city_description_get__oai)

router.get(
    "/climate",
    summary="Get city climate.",
    response_model=APICityClimateList,
    name="city-climate-get",
    status_code=status.HTTP_200_OK,
)(views.city_climate_get)

router.get(
    "/climate/oai",
    summary="Get city climate from OpenAI.",
    response_model=APICityClimateList,
    name="city-climate-get-oai",
    status_code=status.HTTP_200_OK,
)(views.city_climate_get__oai)
