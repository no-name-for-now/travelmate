from fastapi import APIRouter
from fastapi import status

from api.models.city_climate import APICityClimateList
from api.models.city_descriptors import CityDescriptorsContract
from api.models.world_cities import APIWorldCitiesActiveList
from api.views import city as views
from tripagenda.routers import responses


city_router = APIRouter(
    prefix="/city",
    tags=["city"],
    responses=responses,
)

cities_router = APIRouter(
    prefix="/cities",
    tags=["cities"],
    responses=responses,
)

# City endpoints
city_router.get(
    "/description",
    summary="Get city description.",
    response_model=CityDescriptorsContract,
    name="city-description-get",
    status_code=status.HTTP_200_OK,
)(views.city_description_get)

city_router.get(
    "/description/oai",
    summary="Get city description from OpenAI.",
    response_model=CityDescriptorsContract,
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

# Cities endpoints
cities_router.get(
    "/active",
    summary="Get all active cities.",
    response_model=APIWorldCitiesActiveList,
    name="cities-active-get",
    status_code=status.HTTP_200_OK,
)(views.cities_active_get)
