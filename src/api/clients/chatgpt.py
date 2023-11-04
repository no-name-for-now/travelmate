"""OpenAI API client."""
import json
from datetime import datetime
from typing import Any
from typing import Dict

import openai
from django.conf import settings


class OpenAI:
    """OpenAI API client."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.model = settings.OPENAI_MODEL
        self.api_key = settings.OPENAI_API_KEY
        self.client = openai
        self.client.api_key = self.api_key

    def chat_completion_create(self, messages: list) -> dict:
        """Create a chat completion."""
        try:
            response = self.client.ChatCompletion.create(
                model=self.model,
                messages=messages,
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

    def get_city_description(self, country, region_string) -> Dict[Any, Any]:
        """Get a city description from OpenAI."""
        init = "Create a 100 word description of {0}, {1} for a tourist".format(
            country, region_string
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

    def get_itenerary(self, country, cities_regions, num_days) -> Dict[Any, Any]:
        """Get an itenerary from OpenAI."""
        init = "Create a travel itenarary in json for {0} days in {1}, add these specific regions or cities: {2}.".format(
            num_days, country, cities_regions
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
