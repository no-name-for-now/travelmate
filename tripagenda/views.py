from django.conf import settings
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


class Wake(BaseModel):
    status: int
    message: str

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            status=d["status"],
            message=d["message"],
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
        }


def healthcheck() -> HealthCheck:
    """
    Return a healthcheck object.
    """
    return HealthCheck(
        status=200,
        version=settings.APP_VERSION,
    )


def wake() -> Wake:
    """
    Return a wake object.
    """
    return Wake(
        status=200,
        message="Ok, I'm up!",
    )
