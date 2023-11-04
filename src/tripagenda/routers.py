from api.utils.http import responses
from fastapi import APIRouter
from fastapi import status
from tripagenda.healthcheck import HealthCheck
from tripagenda.healthcheck import healthcheck


router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    responses=responses,
)

router.get(
    "/",
    summary="Check if the API is up and running.",
    response_model=HealthCheck,
    name="healthcheck-get",
    status_code=status.HTTP_200_OK,
)(healthcheck)
