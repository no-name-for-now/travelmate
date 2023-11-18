"""OpenAI API client."""
import json
from datetime import datetime
from typing import Any
from typing import Dict

import openai
from django.conf import settings

from api.clients.contracts.city_climate import CityClimateOpenAIContract
from api.clients.contracts.city_item import CityItemOpenAIContract
from api.clients.contracts.itinerary import ItineraryOpenAIContract


class OpenAI:
    """OpenAI API client."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.model = settings.OPENAI_MODEL
        self.api_key = settings.OPENAI_API_KEY
        self.client = openai
        self.client.api_key = self.api_key

    def chat_completion_create(self, messages: list, **kwargs) -> dict:
        """
        Create a chat completion.

        Parameters
        ----------
        messages : list
            list of messages to send to OpenAI
        **kwargs : dict
            additional arguments to pass to the OpenAI API
            expected keys: functions: array, function_call: dict

        """
        try:
            response = self.client.ChatCompletion.create(
                model=self.model, messages=messages, **kwargs
            )

            if kwargs.get("functions", None):
                message = response.choices[0]["message"]
                data_string = message["function_call"]["arguments"]
                data = json.loads(data_string)
                return data

            message = response.choices[0]["message"]
            content = json.loads(message["content"])
            return content
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

        init = "Create a 100 word description of the city {0} in country {1}, for a tourist".format(
            city, country
        )

        messages = [
            {"role": "system", "content": "You are a travel assistant."},
            {
                "role": "user",
                "content": init,
            },
        ]

        functions = [
            {
                "name": "get_answer_for_user_query",
                "description": "Get user answer in series of steps",
                "parameters": CityDescriptionOpenAIContract.model_json_schema(),
            }
        ]

        function_call = {"name": "get_answer_for_user_query"}

        return self.chat_completion_create(
            messages, **{"functions": functions, "function_call": function_call}
        )

    def get_itinerary(self, **kwargs) -> Dict[Any, Any]:
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
                "content": init,
            },
        ]

        functions = [
            {
                "name": "get_answer_for_user_query",
                "description": "Get user answer in series of steps",
                "parameters": ItineraryOpenAIContract.model_json_schema(),
            }
        ]

        function_call = {"name": "get_answer_for_user_query"}

        return self.chat_completion_create(
            messages, **{"functions": functions, "function_call": function_call}
        )

    def get_city_climate(self, **kwargs) -> Dict[Any, Any]:
        """Get a city's climate from OpenAI."""
        country = kwargs.get("country")
        city = kwargs.get("city")

        init = "Monthly return of The Avg Rainfall (mm), Avg Low (C) as, Avg High (C) for {0}, {1}, don't return the measurement unit.".format(
            country, city
        )

        messages = [
            {"role": "system", "content": "You are a Meteorology Analyst."},
            {
                "role": "user",
                "content": init,
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

        return self.chat_completion_create(
            messages, **{"functions": functions, "function_call": function_call}
        )

    def get_city_items(self, **kwargs) -> Dict[Any, Any]:
        """Get a city's climate from OpenAI."""
        country = kwargs.get("country")
        city = kwargs.get("city")

        init = """Please give met the top 20 things to do, with a tag like adventure, culinary, historical,
                        art, cultural, night life etc and the recommended time to spend at the
                        activity for the city: {1}, {0}""".format(
            country, city
        )

        messages = [
            {"role": "system", "content": "You are a Travel Guide."},
            {
                "role": "user",
                "content": init,
            },
        ]

        functions = [
            {
                "name": "get_answer_for_user_query",
                "parameters": CityItemOpenAIContract.model_json_schema(),
            }
        ]

        function_call = {"name": "get_answer_for_user_query"}

        return self.chat_completion_create(
            messages, **{"functions": functions, "function_call": function_call}
        )
