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
password = 'postgresqladmin'  # Ideally this would come from config.py (or similar)
database_name = 'rental_db' # We'll use the Pagila database from Class 9.2
port_number = '5433' # Check your own port number! It's probably 5432, but it might be different!
connection_string = f'postgresql://{username}:{password}@localhost:{port_number}/{database_name}'

# Connect to the SQL database
engine = create_engine(connection_string)
base = automap_base()
base.prepare(engine, reflect=True)

# Choose the SQL table we wish to use. As we discussed in class, your tables
# won't be available via reflection unless they contain a primary key. 
table = base.classes.film

# OPTIONAL - For MongoDB Use Only
import pymongo 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.geojson_db 

# Instantiate the Flask application. (Chocolate cake recipe.)
# This statement is required for Flask to do its job. 
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # Effectively disables page caching

# Here's where we define the various application routes. Note that the name
# of a route must NEVER include the IP address (e.g., 127.0.0.1), and shouldn't
# include the file extension either; i.e., use "my_route" as the name of the route,
# not "my_route.html" and definitely not "127.0.0.1:5000/my_route."
@app.route("/")
def IndexRoute():
    ''' Runs when the browser loads the index route (i.e., the "home page"). 
        Note that the html file must be located in a folder called templates. '''

    webpage = render_template("index.html")
    return webpage

@app.route("/other")
def OtherRoute():
    ''' Runs when the user clicks the link for the other page.
        Note that the html file must be located in a folder called templates. '''

    # Note that this call to render template passes in the title parameter. 
    # That title parameter is a 'Shirley' variable that could be called anything 
    # we want. The name has to match the parameter used in other.html. We could 
    # pass in lists, dictionaries, or other values as well. And we don't have 
    # to pass in anything at all (which would make a lot more sense in this case).
    webpage = render_template("other.html", title_we_want="Shirley")
    return webpage

@app.route("/map")
def MapRoute():
    ''' Loads the NYC Boroughs map that comes from Class 15.2, Activity 01. '''

    webpage = render_template("map.html")
    return webpage

@app.route("/film")
def FilmRoute():
    ''' Queries the Pagila database from Class 9.2 for film information. '''

    # Open a session, run the query, and then close the session again
    session = Session(engine)
    results = session.query(table.film_id, table.title, table.description).all()
    session.close()

    # Create a list of dictionaries, with each dictionary containing one row from the query. 
    film_info = []
    for id, title, description in results:
        dict = {}
        dict["id"] = id
        dict["title"] = title
        dict["description"] = description
        film_info.append(dict)

    # Return the jsonified result. 
    return jsonify(film_info)

@app.route("/test")
def TestRoute():
    ''' Returns a simple text message, just to test whether 
        the Flask server is working. '''

    # You wouldn't build a route this way in real life. 

    return "This is the test route!"

@app.route("/dictionary")
def DictionaryRoute():
    ''' Returns a properly jsonified dictionary. '''

    dict = { "Fine Sipping Tequila": 10,
             "Beer": 2,
             "Red Wine": 8,
             "White Wine": 0.25 }
    
    return jsonify(dict) # Return the jsonified version of the dictionary

@app.route("/dict")
def DictRoute():
    ''' Does it WRONG and returns a dictionary directly.'''        

    dict = { "one": 1,
             "two": 2,
             "three": 3 }
    
    return dict # WRONG! Don't return a dictionary! Ever! Return a JSON instead. 
  
@app.route("/readjsonfile/<filename>")
def ReadJsonFileRoute(filename):    
    ''' Opens a JSON or GeoJSON file and then returns
        its contents to the client. The filename is specified
        as a parameter. '''

    # Note that we have to assemble the complete filepath. We do this on the 
    # server because the client has no knowledge of the server's file structure.
    filepath = f"static/data/{filename}"

    # Add some simple error handling to help if the user entered an invalid
    # filename. 
    try: 
        with open(filepath) as f:    
            json_data = json.load(f)
    except:
        json_data = {'Error': f'{filename} not found on server!'}

    print('Returning data from a file')

    return jsonify(json_data)

@app.route("/readmongodb")
def ReadMongoDB():
    ''' Queries MongoDB for all entries in the maps collection and then
        returns the first one to the user. '''

    # Query the maps table
    result = db.maps.find()

    # Note: MongoDB operates on BSONs, which are binary JSONs, and the '_id' in 
    # each 'document' is really a pointer (think: memory location) to additional
    # data that makes the database work. That pointer will cause an error when
    # you try to jsonify() the raw data that gets returned from a MongoDB query. 
    #
    # One solution is simply to remove the '_id' from the 'document' 
    # and throw it away, which is what we'll do here. The 
    # remaining 'document' can then be jsonified. 

    result_list = list(result)
    if len(result_list) > 0:
        # Return the first result only and strip off the '_id'
        data = result_list[0] 
        id_to_discard = data.pop('_id', None)
    else:
        # Construct an error message
        data = {'Error': 'No data found'}        

    print('Returning data from MongoDB')

    return jsonify(data)

   

# This statement is required for Flask to do its job. 
# Think of it as chocolate cake recipe. 
if __name__ == '__main__':
    app.run(debug=True)