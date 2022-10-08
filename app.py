# Shout out to Dom for a "Chocolate Cake Recipe"

# Import the functions we need from Flask
from flask import Flask
from flask import render_template 
from flask import jsonify

# Import the functions we need from SQL Alchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Import any remaining functions
import json

# Define the PostgreSQL connection parameters
username = 'postgres'  # Ideally this would come from config.py (or similar)
password = 'bootcamp'  # Ideally this would come from config.py (or similar)
database_name = 'AlcoholUnemployment_db'
port_number = '5432' # Check your own port number!
connection_string = f'postgresql://{username}:{password}@localhost:{port_number}/{database_name}'

# Connect to the SQL database
engine = create_engine(connection_string)
base = automap_base()
base.prepare(engine, reflect=True)

table = base.classes.cleaned_combined_data

# This statement is required for Flask to do its job. 
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Index Route
@app.route("/")
def IndexRoute():

    webpage = render_template("index.html")
    return webpage

# DataSet Main Route
@app.route("/countries")
def CountriesRoute():

    session = Session(engine)
    results = session.query(
        table.country,
        table.beer_servings,
        table.spirit_servings,
        table.wine_servings,
        table.total_litres_of_pure_alcohol,
        table.unemployment_rate
    ).all()
    session.close()

    data = []
    for country,beer_servings,spirit_servings,wine_servings,total_litres_of_pure_alcohol,unemployment_rate in results:
        dict = {}
        dict["country"] = country
        dict["beer_servings"] = beer_servings
        dict["spirit_servings"] = spirit_servings
        dict["wine_servings"] = wine_servings
        dict["total_litres_of_pure_alcohol"] = total_litres_of_pure_alcohol
        dict["unemployment_rate"] = unemployment_rate
        data.append(dict)

    #webpage = render_template("dataset1.html")
    return jsonify(data)

# DataSet Specific Route
@app.route("/countries/<filename>")
def CountrySpecificRoute(filename):

    session = Session(engine)
    results = session.query(
        table.country,
        table.beer_servings,
        table.spirit_servings,
        table.wine_servings,
        table.total_litres_of_pure_alcohol,
        table.unemployment_rate
    ).all()
    session.close()

    data = []
    for country,beer_servings,spirit_servings,wine_servings,total_litres_of_pure_alcohol,unemployment_rate in results:
        dict = {}
        dict["country"] = country
        dict["beer_servings"] = beer_servings
        dict["spirit_servings"] = spirit_servings
        dict["wine_servings"] = wine_servings
        dict["total_litres_of_pure_alcohol"] = total_litres_of_pure_alcohol
        dict["unemployment_rate"] = unemployment_rate
        data.append(dict)

    search_term = filename.replace(" ", "").lower()
    for country in data:
        country_name = country["country"].replace(" ", "").lower()

        if search_term == country_name:
            return jsonify(country)

    return jsonify({"error": f"Data for : {search_term} not found."}), 404

# Test Route
@app.route("/map")
def MapRoute():

    webpage = render_template("map.html")
    return webpage

# Run app.py in debug
if __name__ == '__main__':
    app.run(debug=True)