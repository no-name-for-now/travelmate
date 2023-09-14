from datetime import datetime
from flask import Flask, render_template, request
from flask_migrate import Migrate
from helpers.itenerary import get_itenerary, load_config
from database import db
from models import Itenerary, UniqueSearchHistory
from contracts.model_contracts import UniqueSearchHistorySchema, ItenerarySchema
from sqlalchemy.exc import IntegrityError
import pandas as pd
from psycopg2.errors import UniqueViolation
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost/mydatabase'  # Use the same values as in your Docker Compose file
db.init_app(app)
migrate = Migrate(app, db)

config_file = "configs.yaml"
config = load_config(config_file)

def list_tables():
    # Get a list of all tables in the database
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()
    
    return table_names

def query_search_history(country, specific_places, num_days):
    # Use the SQLAlchemy filter method to specify your filter criteria
    data = UniqueSearchHistory.query.filter(
        UniqueSearchHistory.country == country,
        UniqueSearchHistory.specific_places == specific_places,
        UniqueSearchHistory.num_days == num_days
    ).all()
    
    # Process the filtered data (for example, print it)
    for item in data:
        return item.id


@app.route("/query_ush")
def query_ush():
    data = db.session.query(UniqueSearchHistory).all()
    for item in data:
        print(item.id, " ", item.num_days, " ",item.country ," ", item.specific_places)
    return "done"

@app.route("/query_i")
def query_i():
    data = db.session.query(Itenerary).all()
    for item in data:
        print(item.id, " ", item.unique_search_history_id, " ",item.day ," ", item.morning_activity)
    return "done"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        country = request.form["country"]
        region_string = request.form["region_string"].replace(" ", "")
        region_list = region_string.split(",")
        region_list.sort()
        region_string = ','.join(region_list)
        from_date_obj = datetime.strptime(request.form["from"], '%Y-%m-%d')
        to_date_obj = datetime.strptime(request.form["to"], '%Y-%m-%d')
        days = (to_date_obj - from_date_obj).days 
        unique_search_history_schema = UniqueSearchHistorySchema(num_days=days, country=country, specific_places=region_string)
        if unique_search_history_schema.validate_data:  # Custom validation function
            data_dict = unique_search_history_schema.to_dict()
            unique_search_history_data = UniqueSearchHistory(**data_dict)
            try: 
                db.session.add(unique_search_history_data)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback() 
                unique_search_history_id = query_search_history(num_days=days, country=country, specific_places=region_string)
                results = Itenerary.query.filter_by(unique_search_history_id=unique_search_history_id).all()
                test = select(UniqueSearchHistory, Itenerary).join(Itenerary, UniqueSearchHistory.id == Itenerary.unique_search_history_id).where(UniqueSearchHistory.id == unique_search_history_id)
                test_result = db.session.execute(test)
                test_result_df = pd.DataFrame(test_result.fetchall(), columns=test_result.keys())
                print(test_result_df)
                df = pd.DataFrame([result.__dict__ for result in results])
                df = df.drop('_sa_instance_state', axis=1, errors='ignore')
                print(df)
                print("Unique Search History")
                return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)

            df = get_itenerary(country, region_string, days, config)  #need to change this to not use a data frame and just keep the json
            columns = ['index','Travel Method','Travel Time', 'Morning Activity','Afternoon Activity','Evening Activity']
            itenerary_store = df[columns].copy()
            itenerary_store['unique_search_history_id'] = unique_search_history_data.id
            itenerary_store.columns = ['day','travel_method','travel_time','morning_activity','afternoon_activity','evening_activity','unique_search_history_id']
            for index, row in itenerary_store.iterrows():
                itenerary_schema = ItenerarySchema(
                    unique_search_history_id = row['unique_search_history_id'],
                    day = row['day'],
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


            print("stored to itenerary")
            return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)

        else:
            print("data not valid")



    tables = list_tables()
    print("Tables in the database:", tables)
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
