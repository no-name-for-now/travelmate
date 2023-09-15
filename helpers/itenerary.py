import openai
import json
import pandas as pd
import yaml

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

def load_config(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.safe_load(stream)
    return config
