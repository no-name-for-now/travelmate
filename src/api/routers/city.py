from api.models.city_climate import APICityClimateList
from api.models.city_descriptors import APICityDescriptorsList
from api.models.world_cities import WorldCitiesActiveContract
from api.views import city as views
from fastapi import APIRouter
from fastapi import status
from tripagenda.routers import responses


city_router = APIRouter(
    prefix="/city",
    tags=["city"],
    responses=responses,
)

city_router.get(
    "/description",
    summary="Get city description.",
    response_model=APICityDescriptorsList,
    name="city-description-get",
    status_code=status.HTTP_200_OK,
)(views.city_description_get)

city_router.get(
    "/description/oai",
    summary="Get city description from OpenAI.",
    response_model=APICityDescriptorsList,
    name="city-description-get-oai",
    status_code=status.HTTP_200_OK,
)(views.city_description_get__oai)

city_router.get(
    "/climate",
    summary="Get city climate.",
    response_model=APICityClimateList,
    name="city-climate-get",
    status_code=status.HTTP_200_OK,
)(views.city_climate_get)

city_router.get(
    "/climate/oai",
    summary="Get city climate from OpenAI.",
    response_model=APICityClimateList,
    name="city-climate-get-oai",
    status_code=status.HTTP_200_OK,
)(views.city_climate_get__oai)

cities_router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    responses=responses,
)

cities_router.get(
    "/active",
    summary="Get all active cities.",
    response_model=WorldCitiesActiveContract,
    name="cities-active-get",
    status_code=status.HTTP_200_OK,
)(views.cities_active_get)
