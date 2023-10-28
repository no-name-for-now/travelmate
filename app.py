from flask import Flask, request, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector, IPTypes
from models import Itenerary, UniqueSearchHistory, SearchHistory, WorldCities, CityDescriptors, UserSavedItinerary
from contracts.model_contracts import UniqueSearchHistorySchema, ItenerarySchema, CityDescriptorSchema
from crud.read import list_tables, query_search, most_searched, query_search_fe
from crud.write import insert_data
from helpers.api_validators import validate_first_backend, validate_get_city_description, validate_store_user_search
from helpers.ipfunctions import get_ip
from helpers.itenerary import itinerary_vars, get_itenerary, get_city_description_chatgpt
from helpers.get_secret import get_secret
from sqlalchemy.exc import IntegrityError, DatabaseError
from database import db
import pg8000
import json
import os



# initialize Python Connector object
connector = Connector()

config = {}
config["api_key"] = get_secret("resolute-tracer-402011", "api_key")
config["db_host"] = get_secret("resolute-tracer-402011", "db_host")
config["db_password"] = get_secret("resolute-tracer-402011", "db_password")
config["db_user"] = get_secret("resolute-tracer-402011", "db_user")

# Python Connector database connection function
def getconn():
    conn = connector.connect(
        "resolute-tracer-402011:europe-west1:travelmate-backend-gpt", # Cloud SQL Instance Connection Name
        "pg8000",
        user=f'{config["db_user"]}',
        password=f'{config["db_password"]}',
        db="postgres",
        ip_type= IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
    )
    return conn


#app = Flask(__name__, static_folder='../travelmate-fe/build')
app = Flask(__name__)



limiter = Limiter(get_ip, app=app, storage_uri="memory://")


env = os.getenv('environment', default=None)
print(env)
if env == 'DEV':
    CORS(app)
else:
    CORS(app, origins=["https://travelagenda-fe.web.app","https://www.travelagenda-fe.web.app","https://tripagenda.co","https://www.tripagenda.co"])

# configure Flask-SQLAlchemy to use Python Connector
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}

# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)



@app.route("/db_health", methods=["GET"])
@limiter.limit('5 per minute')
def db_health():
    with app.app_context():  # Ensuring the database operation is within the app context
        city_id = query_search_fe(model=WorldCities, only_id=1, city='Brussels')
        return str(city_id)

@app.route("/store_user_search", methods=["POST"])
@limiter.limit('5 per minute')
def store_user_search():
    data=request.json
    if validate_store_user_search(data) is False:
        return None

    try:
        user_saved_itinerary = UserSavedItinerary(**data)
        db.session.add(user_saved_itinerary)
        db.session.commit()
    except DatabaseError as e:
        db.session.rollback() 
        return "Data Already Stored"


    #UserSavedItinerary

    return "awe"



@app.route("/get_city_description", methods = ["POST"])
@limiter.limit('15 per minute')
def get_city_description():
    data = request.json
    if validate_get_city_description(data) is False:
        return None
    country = data.get("country").replace(" ", "")
    city = data.get("cities").replace(" ", "")
    city_id = query_search_fe(model = WorldCities,only_id = 1, city=city)

    city_description = query_search_fe(model = CityDescriptors,only_id = 0, city_id=city_id)
    if city_description == "[]":
        df = get_city_description_chatgpt(country = country, region_string=city, config = config)
        city_descriptor_schema = CityDescriptorSchema(city_id = city_id,city_description =  df['description'][0])
        if city_descriptor_schema.validate_data:  # Custom validation function
            data_dict = city_descriptor_schema.to_dict()
            city_descriptor_data = CityDescriptors(**data_dict)
        db.session.add(city_descriptor_data)
        db.session.commit()
        city_description = query_search_fe(model = CityDescriptors,only_id = 0, city_id=city_id)
        return city_description
    else:
        return city_description

@app.route("/first_backend", methods = ["POST"])
@limiter.limit('15 per minute')
def first_backend():
    itenerary_dict = itinerary_vars(request)
    if validate_first_backend(itenerary_dict) is False:
        return None

    unique_search_history_schema = UniqueSearchHistorySchema(num_days=itenerary_dict['days'], country=itenerary_dict['country'], specific_places=itenerary_dict['cities'])
    if unique_search_history_schema.validate_data:  # Custom validation function
        data_dict = unique_search_history_schema.to_dict()
        unique_search_history_data = UniqueSearchHistory(**data_dict)

    try: 
        db.session.add(unique_search_history_data)
        db.session.commit()
    except DatabaseError as e:
        db.session.rollback() 
        unique_search_history_id = query_search_fe(model = UniqueSearchHistory,only_id = 1, num_days=itenerary_dict['days'], country=itenerary_dict['country'], specific_places=itenerary_dict['cities'])
        results = query_search_fe(model = Itenerary, only_id = 0, unique_search_history_id=unique_search_history_id)
        insert_data(SearchHistory, db, {'unique_search_history_id':unique_search_history_id})
        return results

    df = get_itenerary(itenerary_dict['country'], itenerary_dict['cities'], itenerary_dict['days'], config)  #need to change this to not use a data frame and just keep the json
    df['unique_search_history_id'] = unique_search_history_data.id

    for index, row in df.iterrows():
        itenerary_schema = ItenerarySchema(
            unique_search_history_id = row['unique_search_history_id'],
            day = row['day'],
            city = row['specific_places'],
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
            except DatabaseError as e:
                pass
    results = query_search_fe(model = Itenerary,only_id = 0, unique_search_history_id=unique_search_history_data.id)
    insert_data(SearchHistory, db, {'unique_search_history_id': unique_search_history_data.id})

    return results

@app.route("/top10", methods = ["GET"])
def top10():
    results = most_searched(db,SearchHistory,UniqueSearchHistory)
    result_list = [{'country': country, 'city': city, 'itenerary_length': x, 'number_of_searches': y} for country, city, x, y in results]
    result_json = json.dumps(result_list)

    return result_list


@app.route('/remote')
def show_remote_addr():
    remote_addr = request.remote_addr
    return f'Your remote address is 2: {remote_addr}'

if __name__ == "__main__":
    if env == 'DEV':
        app.run(debug=True)
    else:
        app.run()
