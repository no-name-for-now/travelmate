from fastapi import APIRouter
from tripagenda.healthcheck import HealthCheck
from tripagenda.healthcheck import healthcheck


router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    responses={404: {"description": "Not found"}},
)

router.get(
    "/",
    summary="Check if the API is up and running.",
    response_model=HealthCheck,
    name="healthcheck-get",
)(healthcheck)
