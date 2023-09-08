from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from helpers.itenerary import get_itenerary, load_config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/mydatabase'  # Use the same values as in your Docker Compose file

db = SQLAlchemy(app)

config_file = "configs.yaml"
config = load_config(config_file)
print(config)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        country = request.form["country"]
        region_string = request.form["region_string"]
        from_date_obj = datetime.strptime(request.form["from"], '%Y-%m-%d')
        to_date_obj = datetime.strptime(request.form["to"], '%Y-%m-%d')
        days = (to_date_obj - from_date_obj).days 
        #return "<p>Hello, World!</p>"
        df = get_itenerary(country, region_string, days, config)  #need to change this to not use a data frame and just keep the json
        return render_template("itenerary.html",  tables=[df.to_html(classes='data', header="true")], df=df)

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
