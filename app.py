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


@app.route("/first_backend", methods = ["POST"])
def first_backend():
    itenerary_dict = itinerary_vars(request)
    print(itenerary_dict)
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
        print(unique_search_history_id)
        results = query_search_fe(model = Itenerary, unique_search_history_id=unique_search_history_id)
        print(results)


    return results

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        home_request = home_vars(request)
        #home_request = home_vars_locust(request) #use this line to stress test

        unique_search_history_schema = UniqueSearchHistorySchema(num_days=home_request['days'], country=home_request['country'], specific_places=home_request['region_string'])
        if unique_search_history_schema.validate_data:  # Custom validation function
            data_dict = unique_search_history_schema.to_dict()
            unique_search_history_data = UniqueSearchHistory(**data_dict)

            try: 
                db.session.add(unique_search_history_data)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback() 

                unique_search_history_id = query_search(model = UniqueSearchHistory, num_days=home_request['days'], country=home_request['country'], specific_places=home_request['region_string'])
                results = query_search(model = Itenerary, unique_search_history_id=unique_search_history_id)

                df = pd.DataFrame([result.__dict__ for result in results])
                df = df.drop('_sa_instance_state', axis=1, errors='ignore')

                insert_data(SearchHistory, db, {'unique_search_history_id':unique_search_history_id})
                return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)



            df = get_itenerary(home_request['country'], home_request['region_string'], home_request['days'], config)  #need to change this to not use a data frame and just keep the json
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
                        print(itenerary_data.id)
                    except IntegrityError as e:
                        print("Data already in the DB, lets fetch it from the table")
            insert_data(SearchHistory, db, {'unique_search_history_id': unique_search_history_data.id})
            return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)

        else:
            print("data not valid")


    from_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    top10_most_searched = most_searched(db,SearchHistory,UniqueSearchHistory)
    return render_template("home.html", default_from_date=from_date, default_to_date=to_date, top10_most_searched = top10_most_searched, countries=countries, country_cities=country_cities)


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
