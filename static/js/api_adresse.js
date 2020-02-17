var map = L.map('map');

// objet map initialisé
var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

// url pour récupérer les images du fond de carte
var osmAttrib='Map data © OpenStreetMap contributors';

// source de la carte
var osm = new L.TileLayer(osmUrl,{attribution:osmAttrib}).addTo(map);

// afficher des images tuiles, ajout à la carte 
map.setView([45.7,4.7],8);

var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;

var provider = new OpenStreetMapProvider();

var point = [];

var searchControl = new GeoSearchControl({
  provider: provider,
  style: 'bar|button',
  searchLabel: 'Entrer une adresse',
  showPopup: false, 
  marker: {                                           
    //icon: new L.Icon.Default(), -- changer d'icon
    draggable: false
  },
  keepResult: true,
  position: 'topright',
  animateZoom: true,
});

marqueur = L.layerGroup().addTo(map);

function placeMarker(){
   if (typeof searchControl._map._lastCenter !== 'null' & typeof searchControl.resultList.results !== 'undefined') {
      x = searchControl._map._lastCenter.lat;
      y = searchControl._map._lastCenter.lng;
      searchControl.markers.remove();
      marqueur.clearLayers();
      marqueur.addLayer(L.marker([x, y]));
      console.log(searchControl)
    }
}

map.on("zoomend",function(){
  placeMarker()
});

map.on("moveend",function(){
  placeMarker()
});

map.on("click", function(ev){
  x = searchControl._map._lastCenter.lat;
  y = searchControl._map._lastCenter.lng;
  searchControl.markers.remove();
  marqueur.clearLayers();
  marqueur.addLayer(L.marker(ev.latlng));
});

function validate(){
  //do something
};


map.addControl(searchControl);
