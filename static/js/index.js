
var map = L.map('map');

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib='Map data by OpenStreetMap contributors';
map.setView([45.75, 4.8], 11);
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

var parc = $.ajax({
  url:"http://127.0.0.1/sendresultat",
  dataType: "json",
  responseType: "json",
  success: console.log("user successfully loaded."),
  error: function (xhr) {
    alert(xhr.statusText)
  }
});
console.log(parc);
$.when(parc).done(function() {
	console.log(parc);
    map.setView([45.75, 4.8], 11);
    var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);
    var mydata = parc.responseJSON;
    var mymapdata = L.geoJSON(mydata).addTo(map);
});
