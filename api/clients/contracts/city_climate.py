from typing import List

from pydantic import BaseModel


class CityClimateOpenAIContract(BaseModel):
    """City Climate response from OpenAI contract."""

    city: str
    month: List[str]
    low: List[float]
    high: List[float]
    rainfall: List[float]

    @classmethod
    def from_model(cls, instance) -> "CityClimateOpenAIContract":
        """Convert a Django CityClimateORM model instance to an APICityClimate instance."""
        return cls(
            city=instance.city,
            month=instance.month,
            low=instance.low,
            high=instance.high,
            rainfall=instance.rainfall,
        )

    def to_dict(self):
        return {
            "city": self.city,
            "month": self.Month,
            "low": self.Low,
            "high": self.High,
            "rainfall": self.Rainfall,
        }
