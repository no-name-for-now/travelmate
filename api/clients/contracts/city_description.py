from pydantic import BaseModel


class CityDescriptionOpenAIContract(BaseModel):
    city: str
    description: str
