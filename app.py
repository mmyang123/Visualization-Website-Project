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
#username = 'postgres'  # Ideally this would come from config.py (or similar)
#password = 'bootcamp'  # Ideally this would come from config.py (or similar)
#database_name = 'rental_db'
#port_number = '5432' # Check your own port number!
#connection_string = f'postgresql://{username}:{password}@localhost:{port_number}/{database_name}'

# Connect to the SQL database
#engine = create_engine(connection_string)
#base = automap_base()
#base.prepare(engine, reflect=True)

#table = base.classes.database

# This statement is required for Flask to do its job. 
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Index Route
@app.route("/")
def IndexRoute():

    webpage = render_template("index.html")
    return webpage

# DataSet 1 Route
@app.route("/dataset1")
def DataSet1Route():

    webpage = render_template("dataset1.html")
    return webpage

#DataSet 2 Route
@app.route("/dataset2")
def DataSet2Route():

    webpage = render_template("dataset2.html")
    return webpage

# Run app.py in debug
if __name__ == '__main__':
    app.run(debug=True)