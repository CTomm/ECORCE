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

map.addControl(searchControl);