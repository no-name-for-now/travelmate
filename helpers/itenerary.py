import openai
import json
import pandas as pd
import yaml
from datetime import datetime
from .string_operators import sort_csv

def get_itenerary(country, region_string, n_days, config):
    openai.api_key = config["api_key"]
    model_engine = config['model_engine']
    message_first_part = "Create a travel itenarary in json for {0} days in {1}, add these specific regions or cities: {2}.".format(n_days, country, region_string)
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": message_first_part + """
                Respond in the following format: {Day : n,
                                                            {Overnight City: , 
                                                             Travel Method : , 
                                                             Travel Time : , 
                                                             Morning Activity : , 
                                                             Afternoon Activity : , 
                                                             Evening Activity : }}"""},
        ])
    
    message = response.choices[0]['message']
    object = json.loads(message['content'])
    df = pd.DataFrame.from_dict(object).T.reset_index()
    df['country'] = country
    df['specific_places'] = region_string
    df.columns = ['day','city','travel_method','travel_time','morning_activity','afternoon_activity','evening_activity','country','specific_places']

    return df


def get_city_description_chatgpt(country, region_string, config):
    openai.api_key = config["api_key"]
    model_engine = config['model_engine']
    message_first_part = "Create a create a 100 word description of {0}, {1} for a tourist".format(country, region_string)
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a travel assistant."},
            {"role": "user", "content": message_first_part + 'Respond in the following format: {"city": ,"description":}}'},
        ])
    
    message = response.choices[0]['message']
    object = json.loads(message['content'])
    df = pd.DataFrame([object])

    return df


def itinerary_vars(request):
    data = request.json
    country = data.get("country").replace(" ", "")
    cities = data.get("cities").replace(" ", "").replace(" ", "")
    cities = sort_csv(cities)
    from_date_obj = datetime.strptime(data.get("from"), '%Y-%m-%d')
    to_date_obj = datetime.strptime(data.get("to"), '%Y-%m-%d')
    days = (to_date_obj - from_date_obj).days 

    var_dict = {'country' : country, 'cities' : cities, 'from_date_obj':from_date_obj , 'to_date_obj':to_date_obj, 'days':days }

    return var_dict

def home_vars(request):
    country = request.form["country"].replace(" ", "")
    region_string = request.form["region_string"].replace(" ", "")
    region_string = sort_csv(region_string)
    from_date_obj = datetime.strptime(request.form["from"], '%Y-%m-%d')
    to_date_obj = datetime.strptime(request.form["to"], '%Y-%m-%d')
    days = (to_date_obj - from_date_obj).days 

    var_dict = {'country' : country, 'region_string' : region_string, 'from_date_obj':from_date_obj , 'to_date_obj':to_date_obj, 'days':days }

    return var_dict

def home_vars_locust(request):
    data = request.json
    country = data.get("country").replace(" ", "")
    region_string = data.get("region_string").replace(" ", "").replace(" ", "")
    region_string = sort_csv(region_string)
    from_date_obj = datetime.strptime(data.get("from"), '%Y-%m-%d')
    to_date_obj = datetime.strptime(data.get("to"), '%Y-%m-%d')
    days = (to_date_obj - from_date_obj).days 

    var_dict = {'country' : country, 'region_string' : region_string, 'from_date_obj':from_date_obj , 'to_date_obj':to_date_obj, 'days':days }

    return var_dict


def load_config(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config
