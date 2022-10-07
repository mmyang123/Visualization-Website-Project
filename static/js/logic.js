// IMPORTANT: Use one of the following endpoints to read the GeoJSON data 
// from the Flask server. Again, remember that the JavaScript code never
// talks directly to the database. It talks to the server instead, and it
// does so using an API endpoint. 

// This endpoint will read GeoJSON data from a file called nyc.geojson that
// resides on the server. Note that 'readjsonfile' is the name of the route 
// in app.py, while 'nyc.geojson' is the name of the file we want. Note that
//  we're not providing any sort of path to that file, we're simply giving
// the filename. We do it that way because this code runs as the client, and
// the client has no idea where on the server the file is actually stored.
// We let Flask figure out that piece for us (see app.py). 
const file_endpoint = "readjsonfile/nyc.geojson"; 

// This endpoint will read the GeoJSON from MongoDB. For this to work,
// you must first load the GeoJSON data into MongoDB by running the provided 
// Jupyter notebook. See the README.md for more information. Note: Loading
//  the data only has to happen once! From then on, it's remembered in the
// database. 
const mongodb_endpoint = "readmongodb"; 

// IMPORTANT: Now, choose which of these two endpoints to use! 
let url = file_endpoint; 

// Create the map object
let myMap = L.map("map", {
  center: [40.7128, -74.0059],
  zoom: 11
});

// Add the tile layer - Note that we're using the Mapbox tile later for this example, which requires
//                      an account on www.mapbox.com. In class, we used OpenStreets, which does not 
//                      require an API key. 
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// Get the GeoJSON data and plot it on the map
d3.json(url).then(function(data) {
  L.geoJson(data).addTo(myMap);
});
