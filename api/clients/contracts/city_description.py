from pydantic import BaseModel


class CityDescriptionOpenAIContract(BaseModel):
    city_name: str
    city_description: str
