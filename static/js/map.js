let myMap = L.map("map", {
    center: [0, 0],
    zoom: 3
});

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

d3.json("/static/data/countries.geojson").then(function(data){

    console.log(data);

    L.geoJson(data, {
        style: function(feature) {
          return {
            color: "black",
            fillColor: "white",
            fillOpacity: 0.5,
            weight: 1.5
          };
        },
        onEachFeature: function(feature, layer) {
            layer.bindPopup("<h5>" + feature.properties.ADMIN + "</h5>");
        }
    }).addTo(myMap);
});