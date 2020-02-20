
var map = L.map('map');

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib='Map data by OpenStreetMap contributors';
map.setView([45.75, 4.8], 11);
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

$.get( "/sendresultat", function(parc) {
	console.log(parc);
    var mymapdata = L.geoJSON(parc).addTo(map);
});

$.get( "/change", function(elect) {
	console.log(elect);
    document.getElementById("Q9-A").value = parseInt(elect)
});

function show(){
	$.get( "/sendmoyenne", function(moy) {
		console.log(moy);
	    var mymoy = L.geoJSON(moy, {color: 'red'}).addTo(map);
	});
}

