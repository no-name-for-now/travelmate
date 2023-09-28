from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS #DEV ONLY
from flask_migrate import Migrate
from helpers.itenerary import get_itenerary, load_config, home_vars, home_vars_locust, itinerary_vars
from database import db
from models import Itenerary, UniqueSearchHistory, SearchHistory, WorldCities
from contracts.model_contracts import UniqueSearchHistorySchema, ItenerarySchema
from sqlalchemy.exc import IntegrityError
import pandas as pd
from psycopg2.errors import UniqueViolation
from sqlalchemy import select
from crud.read import list_tables, query_search, most_searched, query_search_fe
import json


app = Flask(__name__)
CORS(app) #DEV ONLY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydatabase'  # Use the same values as in your Docker Compose file
db.init_app(app)
migrate = Migrate(app, db)

config_file = "configs.yaml"
config = load_config(config_file)

with app.app_context():
    unique_countries = db.session.query(WorldCities.country).distinct().order_by(WorldCities.country).all()
    countries = [country[0] for country in unique_countries]
    country_cities = {}
    for country in countries:
        cities = WorldCities.query.filter_by(country=country).all()
        country_cities[country] = [city.city for city in cities]

@app.route("/query_sh")
def query_sh():
    data = db.session.query(SearchHistory).all()
    for item in data:
        print(item.id, " ", item.unique_search_history_id, item.created_at, " ",item.updated_at)
    return "done"

@app.route("/query_wc")
def query_wc():
    data = db.session.query(WorldCities).all()
    for item in data:
        print(item.city)
    return "done"

@app.route("/query_ush")
def query_ush():
    data = db.session.query(UniqueSearchHistory).all()
    for item in data:
        print(item.id, " ", item.num_days, " ",item.country ," ", item.specific_places," ", item.created_at, " ",item.updated_at)
    return "done"

@app.route("/query_i")
def query_i():
    data = db.session.query(Itenerary).all()
    for item in data:
        print(item.id, " ", item.unique_search_history_id, " ",item.day ," ", item.morning_activity," ", item.created_at, " ",item.updated_at)
    return "done"

@app.route("/query_tables")
def query_tables():
    tables = list_tables(db)
    print(tables)
    return "done"

def insert_data(model,db,dict):
    data = model(**dict)
    db.session.add(data)
    db.session.commit()

@app.route("/top10", methods = ["GET"])
def top10():
    results = most_searched(db,SearchHistory,UniqueSearchHistory)
    result_list = [{'country': country, 'city': city, 'itenerary_length': x, 'number_of_searches': y} for country, city, x, y in results]
    result_json = json.dumps(result_list)

    return result_list


@app.route("/first_backend", methods = ["POST"])
def first_backend():
    itenerary_dict = itinerary_vars(request)
    unique_search_history_schema = UniqueSearchHistorySchema(num_days=itenerary_dict['days'], country=itenerary_dict['country'], specific_places=itenerary_dict['cities'])
    if unique_search_history_schema.validate_data:  # Custom validation function
        data_dict = unique_search_history_schema.to_dict()
        unique_search_history_data = UniqueSearchHistory(**data_dict)

    try: 
        db.session.add(unique_search_history_data)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback() 
        unique_search_history_id = query_search_fe(model = UniqueSearchHistory, num_days=itenerary_dict['days'], country=itenerary_dict['country'], specific_places=itenerary_dict['cities'])
        results = query_search_fe(model = Itenerary, unique_search_history_id=unique_search_history_id)
        insert_data(SearchHistory, db, {'unique_search_history_id':unique_search_history_id})

        return results

    df = get_itenerary(itenerary_dict['country'], itenerary_dict['cities'], itenerary_dict['days'], config)  #need to change this to not use a data frame and just keep the json
    df['unique_search_history_id'] = unique_search_history_data.id

    for index, row in df.iterrows():
        itenerary_schema = ItenerarySchema(
            unique_search_history_id = row['unique_search_history_id'],
            day = row['day'],
            city = row['city'],
            travel_method = row['travel_method'],
            travel_time = row['travel_time'],
            morning_activity = row['morning_activity'],
            afternoon_activity = row['afternoon_activity'],
            evening_activity = row['evening_activity'])
        if itenerary_schema.validate_data:  # Custom validation function
            data_dict = itenerary_schema.to_dict()
            itenerary_data = Itenerary(**data_dict)                   
            try: 
                db.session.add(itenerary_data)
                db.session.commit()
            except IntegrityError as e:
                pass
    results = query_search_fe(model = Itenerary, unique_search_history_id=unique_search_history_data.id)
    insert_data(SearchHistory, db, {'unique_search_history_id': unique_search_history_data.id})

    return results


@app.route("/", methods=["GET", "POST"])
def home():
    return "Healthy"


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
