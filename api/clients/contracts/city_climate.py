from typing import List

from pydantic import BaseModel


class CityClimateOpenAIContract(BaseModel):
    """City Climate response from OpenAI contract."""

    Month: List[str]
    Low: List[float]
    High: List[float]
    Rainfall: List[float]

    @classmethod
    def from_model(cls, instance) -> "CityClimateOpenAIContract":
        """Convert a Django CityClimateORM model instance to an APICityClimate instance."""
        return cls(
            Month=instance.month,
            Low=instance.low,
            High=instance.high,
            Rainfall=instance.rainfall,
        )

    def to_dict(self):
        return {
            "Month": self.Month,
            "Low": self.Low,
            "High": self.High,
            "Rainfall": self.Rainfall,
        }
