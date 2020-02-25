//var map = L.map('map');

/*----------- MAP ----------------*/

var map = L.map('map', {
    center: [45.75, 4.8],
	minZoom: 0,
    maxZoom: 20,
    zoom: 12
});

var StadiaAttib='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var Stadia_AlidadeSmooth = new L.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {attribution: StadiaAttib}).addTo(map);

/*----------- STYLE ----------------*/
var stylemoy = {
	"color": "#D7833A",
	"weight": 0.8, 
	"opacity": 0,
	"fillOpacity": 1
};

var styleb = {
	"color": "#004E2B",
	"fillOpacity": 1,
	"weight": 0.8, 
	"opacity": 0
};

var stylea = {
	"color": "#93A285",
	"fillOpacity": 1,
	"weight": 0.8, 
	"opacity": 0
};

var stylecom = {
	"color": 'white',
	"fillOpacity": 0.2,
	"weight": 1.5, 
	"opacity": 1
};

function createCustomIcon (feature, latlng) {
  let locIcon = L.icon({
  iconUrl: 'image/marker.png',
  iconSize: [38, 38],
  iconAnchor: [19, 38]
  })
  return L.marker(latlng, { icon: locIcon })
};

let myLayerOptions = {
  pointToLayer: createCustomIcon
};


/*----------- LAYERS ----------------*/

$.post( "/sendresultat", {
	position: localStorage.getItem('position')}, 
	function(parc) {
	//console.log(localStorage.getItem('position'));
    var conso_a = L.geoJSON(parc,{style:stylea}).addTo(map);
    controlLayers.addOverlay(conso_a, "<span style='color: black';'font:14px'>Consommation actuelle</span>") 
});



function resend(){
	console.log("hello")
	//Vegetarien ou non
	if (document.getElementsByName("Q0")[0].checked == true){
		regime = document.getElementsByName("Q0")[0].value;
	}
	else if (document.getElementsByName("Q0")[1].checked == true){
		regime = document.getElementsByName("Q0")[1].value;
	}
	
	//Legumes sous serre ou de saison
	if (document.getElementsByName("Q7b")[0].checked == true){
		legume = document.getElementsByName("Q7b")[0].value;
	}
	else if (document.getElementsByName("Q7b")[1].checked == true){
		legume = document.getElementsByName("Q7b")[1].value;
	}

	//Voiture ou TC
	if (document.getElementsByName("Q18")[0].checked == true){
		voiture = document.getElementsByName("Q18")[0].value;
	}
	else if (document.getElementsByName("Q18")[1].checked == true){
		voiture = document.getElementsByName("Q18")[1].value;
	}

	//Energie
	if (document.getElementsByName("Q19")[0].checked == true){
		energie = document.getElementsByName("Q19")[0].value;
	}
	else if (document.getElementsByName("Q19")[1].checked == true){
		energie = document.getElementsByName("Q19")[1].value;
	}
	else if (document.getElementsByName("Q19")[2].checked == true){
		energie = document.getElementsByName("Q19")[2].value;
	}
	else if (document.getElementsByName("Q19")[3].checked == true){
		energie = document.getElementsByName("Q19")[3].value;
	}
	//console.log(regime);
	if (localStorage.getItem('viande')==null){
		viande = 0
	} else{
		viande = localStorage.getItem('viande')
	}

    $.post( "/change", {
      regime: regime,
      new_legume: legume,
      new_voiture: voiture,
      new_energie: energie,
      new_avion: document.getElementById('Q17-A').value,
      legume: localStorage.getItem('legume'),
      voiture: localStorage.getItem('voiture'),
      avion: localStorage.getItem('avion'),
      viande: viande,
      energie: localStorage.getItem('energie'),
      position:localStorage.getItem('position')
      },
      function(newparc) {
		console.log('new :'+newparc);
	    var conso_b = L.geoJSON(newparc,{style:styleb}).addTo(map);
	    controlLayers.addOverlay(conso_b, "<span style='color: black';'font:14px'>Consommation modifiée</span>") 
	});
};

function moy(){
	$.post( "/sendmoyenne", {
	position: localStorage.getItem('position')},
	function(consomoy) {
		console.log(localStorage.getItem('position'));
	    var conso_moy = L.geoJSON(consomoy,{style:stylemoy}).addTo(map);
	    controlLayers.addOverlay(conso_moy, "<span style='color: black';'font:14px'>Consommation d'un français moyen</span>") 
	});
};
/*var conso_a = L.geoJSON(consoa,{style:stylea}).addTo(map);
var conso_moy = L.geoJSON(consomoy,{style:stylemoy}).addTo(map);
var conso_b = L.geoJSON(consob,{style:styleb}).addTo(map);*/
var commune = L.geoJSON(commune,
	{style:stylecom}).addTo(map);


var loc = L.geoJSON(loc, myLayerOptions).addTo(map);

/*----------- GESTION DES LAYERS-LEGENDE----------------*/

L.control.zoom({
     position:'topright'
}).addTo(map);


var overlays = {
	//"<span style='color: black';'font:14px'>Consommation modifiée</span>": conso_b,
	//"<span style='color: black';'font:14px'>Consommation actuelle</span>": conso_a,
	//"<span style='color: black';'font:14px'>Consommation d'un français moyen</span>": conso_moy,
	//"<span style='color: black';'font:14px'>Adresse</span>": loc,
	"<span style='color: black';'font:14px'>Communes, quartiers</span>": commune
}
var controlLayers = L.control.layers(null, overlays, {collapsed:false}).addTo(map);


var legend = L.control({ position: "bottomright" });

legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += "<h4>Légende</h4>";
  div.innerHTML += '<i style="background: #93A285"></i><span>Votre résultat</span><br>';
  div.innerHTML += '<i style="background: #004E2B"></i><span>Votre résultat modifié</span><br>';
  div.innerHTML += '<i style="background: #D7833A"></i><span>Résultat si vous consommiez<br>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspcomme un français "moyen"</span><br>';
  div.innerHTML += '<i class="icon" ></i><span>Votre adresse</span><br>';
  return div;
};
legend.addTo(map);


$(window).on("beforeunload", function() {
 	fetch( "/leaving");
 	localStorage.clear();
});