"""Basic HTTP response models for API endpoints."""
from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class APIError(BaseModel):
    """API error response error."""

    detail: str = Field(..., description="Error message.")
    code: Optional[int] = Field(None, description="Error code.")
    type: Optional[str] = Field(None, description="Error type.")
    instance: Optional[str] = Field(None, description="Error instance.")

    class Config:
        """Pydantic error configuration."""

        json_schema_extra = {
            "example": {
                "detail": "Error message.",
                "code": 400,
                "type": "Error type.",
                "instance": "Error instance.",
            }
        }

    @classmethod
    def from_error(
        cls,
        obj: Dict[str, Any],
    ):
        """Create an APIError from an error."""
        return cls(
            detail=obj["detail"],
            code=obj["code"],
            type=obj["type"],
            instance=obj["instance"],
        )
