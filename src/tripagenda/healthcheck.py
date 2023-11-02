from django.conf import settings

from fastapi import APIRouter
from pydantic import BaseModel


class HealthCheck(BaseModel):
    status: int
    version: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            status=d["status"],
            version=d["version"],
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "version": self.version,
        }


def healthcheck() -> HealthCheck:
    """
    Returns a healthcheck object.
    """
    return HealthCheck(
        status=200,
        version=settings.APP_VERSION,
    )


router = APIRouter()

router.get(
    "/healthcheck",
    summary="Check if the API is up and running.",
    tags=["healthcheck"],
    response_model=HealthCheck,
    name="healthcheck-get",
)(healthcheck)
