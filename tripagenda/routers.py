from fastapi import APIRouter
from fastapi import status

from api.utils.http import responses
from tripagenda.views import HealthCheck
from tripagenda.views import healthcheck
from tripagenda.views import Wake
from tripagenda.views import wake


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

router.get(
    "/wake",
    summary="Wake up the API.",
    response_model=Wake,
    name="wake",
    status_code=status.HTTP_200_OK,
)(wake)
