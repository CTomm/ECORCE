var map = L.map('map', {
  minZoom: 9
});

// objet map initialisé
var osmUrl='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

// url pour récupérer les images du fond de carte
var osmAttrib='Map data © OpenStreetMap contributors';

// source de la carte
//var osm = new L.TileLayer(osmUrl,{attribution:osmAttrib}).addTo(map);

var CartoDB_Voyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a> &copy; <a href="https://www.flaticon.com/free-icon/marker_1119071?fbclid=IwAR1uUVJ-5rLL4EQ4-kWRcv0pR_cfdP8CMrzAAfLGNl2bi6qSSdaYwX4kAKA"/>Icon made by Eucalyp from www.flaticon.com</a>',
  subdomains: 'abcd'
}).addTo(map);


// afficher des images tuiles, ajout à la carte 
map.setView([45.7,4.7],9);

function style(feature) {
    return {
        weight: 0.8,
        opacity: 0.5,
        //color: '#2A6172',
        color: '#E7498F',
        //dashArray: '1',
        fillOpacity: 0
    };
}


// Info au survol d'une commune / quartier
function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.1
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }

    info.update(layer.feature.properties);
}

function resetHighlight(e) {
    commune.resetStyle(e.target);
    info.update();
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
    });
}

var commune= L.geoJSON(commune, {       
  style:style,
  onEachFeature: onEachFeature
  }).addTo(map);

var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
    this.update();
    return this._div;
};

// method that we will use to update the control based on feature properties passed
info.update = function (properties) {
    this._div.innerHTML = '<h4>Nom de la commune ou du quartier et nombre d\'habitants</h4>' +  (properties ?
        '<b>' + properties.Lieux + '</b><br/>' + properties.pop + ' habitants'
        : 'Survoler une commune ou un quartier');
}

info.addTo(map);

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
    position_user = String(x) + ' ' + String(y);
    document.getElementById("adresse_utilisateur").innerHTML = e.geocode.name;
  })
  .addTo(map);

var position_user = '';

commune.on("click", function(ev){
  marqueur.clearLayers();
  var monmark = L.marker(ev.latlng, {icon:greenIcon})
  marqueur.addLayer(monmark);
  position_user = String(ev.latlng.lng) + ' ' + String(ev.latlng.lat);
  //zoomTo(monmark);
  
  //OSM Nomitatim documentation: http://wiki.openstreetmap.org/wiki/Nominatim , call by jsonQuery
  var jsonQuery = "http://nominatim.openstreetmap.org/reverse?format=json&lat=" + ev.latlng.lat + "&lon=" + ev.latlng.lng + "&zoom=18&addressdetails=1";
     
  $.getJSON(jsonQuery).done( function (result_data) {
    console.log(result_data);
    document.getElementById("adresse_utilisateur").innerHTML = result_data.display_name
  });
});

function send(){
  $.post( "/sendposition", {
    position: position_user
  })
};

/*document.getElementById("conf_quest").onclick = function() {
  document.getElementById("myModal").style.visibility='visible'
};
*/

document.getElementById("conf_quest").onclick = function() {
  if (position_user === '') {
    $('.hover_bkgr_fricc').show();
    $('.hover_bkgr_fricc').click(function(){
        $('.hover_bkgr_fricc').hide();
        document.getElementById("info_map").style.opacity="1";
    });
    $('.popupCloseButton').click(function(){
        $('.hover_bkgr_fricc').hide();
        document.getElementById("info_map").style.opacity="1";
    });
      //alert('Veuillez choisir une adresse svp');
      //document.getElementById("fenetre_alert").style.visibility='visible';
      document.getElementById("info_map").style.opacity="0.5" ;
  } else{
  document.getElementById("fenetre_validation").style.visibility='visible';
  document.getElementById("info_map").style.opacity="0.5";
  }
};

document.getElementById("debut_questionnaire").onclick = function() {
  window.location.href='questionchoix.html'
}