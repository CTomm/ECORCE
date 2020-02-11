
var map = L.map('map');

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib='Map data by OpenStreetMap contributors';

var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

map.setView([45.75, 4.8], 11);

//var utilisateur = L.geoJSON(test).addTo(map);

$.getJSON("127.0.0.1/test", function(data) {
    L.geoJson(data, {
        style: myStyle
    }).addTo(map);
});