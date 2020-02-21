var map = L.map('map', {
  minZoom: 9
});

// objet map initialisé
var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

// url pour récupérer les images du fond de carte
var osmAttrib='Map data © OpenStreetMap contributors';

// source de la carte
var osm = new L.TileLayer(osmUrl,{attribution:osmAttrib}).addTo(map);

// afficher des images tuiles, ajout à la carte 
map.setView([45.7,4.7],9);


var commune= L.geoJSON(commune, {       
  style:style}  
).addTo(map);

function style(feature) {
    return {
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.5
    };
}

//Geocoding queries service using Nominatim with spatial result limitation (viewbox southwest/northeast)
var geocoder = new L.Control.Geocoder.Nominatim({
  geocodingQueryParams: {
      "viewbox": "4.1621,45.3142,5.0952,46.0615", // Bounding box de la couche des communes
      "bounded": "1"
        }
    });


var marqueur = new L.layerGroup().addTo(map);
var greenIcon = L.icon({
    iconUrl: './image/marker.png',
    iconSize:     [40,40] // size of the icon
/*    shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor*/
});

function zoomTo(marker) {
  var latLngs = [ marker.getLatLng() ];
  var markerBounds = L.latLngBounds(latLngs);
  map.fitBounds(markerBounds);
};

var adress = L.Control.geocoder({
  position: "topleft",
  placeholder: "Quelle est votre adresse ?",
  errorMessage: "Aucun résultat trouvé ...",
  geocoder : geocoder,
  expand: "click",
  defaultMarkGeocode: false
})
  .on('markgeocode', function(e) {
    marqueur.clearLayers();
    var x = e.geocode.center.lat;
    var y = e.geocode.center.lng;
    var monmark = L.marker([x, y], {icon:greenIcon})
    marqueur.addLayer(monmark);
    zoomTo(monmark);
  })
  .addTo(map);

commune.on("click", function(ev){
  marqueur.clearLayers();
  var monmark = L.marker(ev.latlng, {icon:greenIcon})
  marqueur.addLayer(monmark);
  position_user = String(ev.latlng.lng) + ' ' + String(ev.latlng.lat);
  //zoomTo(monmark);
});

function send(){
    $.post( "/sendposition", {
      position: position_user
      })
};
