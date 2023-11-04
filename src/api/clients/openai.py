"""OpenAI API client."""
import json
from datetime import datetime
from typing import Any
from typing import Dict

import openai
from api.clients.contracts.city_climate import CityClimateOpenAIContract
from django.conf import settings


class OpenAI:
    """OpenAI API client."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.model = settings.OPENAI_MODEL
        self.api_key = settings.OPENAI_API_KEY
        self.client = openai
        self.client.api_key = self.api_key

    def chat_completion_create(
        self, messages: list, functions: list = [], function_call: dict = {}
    ) -> dict:
        """Create a chat completion."""
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=messages,
                functions=functions,
                function_call=function_call,
            )

            object = json.loads(response.choices[0]["message"])
        except Exception as e:
            object = {
                "error": "Error occurred while fetching from OpenAI API",
                "error_message": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "messages": messages,
            }

        return object

    def get_city_description(self, **kwargs) -> Dict[Any, Any]:
        """Get a city description from OpenAI."""
        country = kwargs.get("country")
        city = kwargs.get("city")

        init = "Create a 100 word description of {0}, {1} for a tourist".format(
            country, city
        )

        messages = [
            {"role": "system", "content": "You are a travel assistant."},
            {
                "role": "user",
                "content": init
                + 'Respond in the following format: {"city": ,"description":}}',
            },
        ]

        return self.chat_completion_create(messages)

    def get_itenerary(self, **kwargs) -> Dict[Any, Any]:
        """Get an itenerary from OpenAI."""
        country = kwargs.get("country")
        city = kwargs.get("city")
        num_days = kwargs.get("num_days")

        init = "Create a travel itenarary in json for {0} days in {1}, add this specific region or city: {2}.".format(
            num_days, country, city
        )

        messages = [
            {"role": "system", "content": "You are a travel assistant."},
            {
                "role": "user",
                "content": init
                + """
            Respond in the following format: {Day : n,
                                                        {Overnight City: ,
                                                        Travel Method : ,
                                                        Travel Time : ,
                                                        Morning Activity : ,
                                                        Afternoon Activity : ,
                                                        Evening Activity : }}""",
            },
        ]

        return self.chat_completion_create(messages)

    def get_city_climate(self, **kwargs) -> Dict[Any, Any]:
        """Get a city's climate from OpenAI."""
        country = kwargs.get("country")
        city = kwargs.get("city")

        init = "Monthly return of The Avg Rainfall (mm), Avg Low (C) as, Avg High (C) for {0}, {1}, dont return the measurement unit.".format(
            country, city
        )

        messages = [
            {"role": "system", "content": "You are a Meteorology Analyst."},
            {
                "role": "user",
                "content": init
                + 'Respond in the following format: {"city": ,"description":}}',
            },
        ]

        functions = [
            {
                "name": "get_answer_for_user_query",
                "description": "Get user answer in series of steps",
                "parameters": CityClimateOpenAIContract.model_json_schema(),
            }
        ]

        function_call = {"name": "get_answer_for_user_query"}

        return self.chat_completion_create(messages, functions, function_call)
