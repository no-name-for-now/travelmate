from datetime import datetime
from flask import Flask, render_template, request
from flask_migrate import Migrate
from helpers.itenerary import get_itenerary, load_config
from database import db
from models import Itenerary, UniqueSearchHistory



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

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        country = request.form["country"]
        region_string = request.form["region_string"]
        region_list = region_string.split(",").sort()
        from_date_obj = datetime.strptime(request.form["from"], '%Y-%m-%d')
        to_date_obj = datetime.strptime(request.form["to"], '%Y-%m-%d')
        days = (to_date_obj - from_date_obj).days 
        df = get_itenerary(country, region_string, days, config)  #need to change this to not use a data frame and just keep the json
        return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)

    tables = list_tables()
    print("Tables in the database:", tables)
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
