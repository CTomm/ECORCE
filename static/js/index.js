var map = L.map('map');

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib='Map data by OpenStreetMap contributors';
map.setView([45.75, 4.8], 11);
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

$.get( "/sendresultat", function(parc) {
	//console.log('old : '+ parc);
    var mymapdata = L.geoJSON(parc).addTo(map);
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
	console.log(regime);

    $.post( "/change", {
      regime: regime,
      legume: legume,
      voiture: voiture,
      energie: energie,
      avion: document.getElementById('Q17-A').value
      },
      function(newparc) {
		console.log('new :'+newparc);
	    var newparc = L.geoJSON(newparc, {color: 'red'}).addTo(map);
	});
};

function moy(){
	$.get( "/sendmoyenne", function(moy) {
		//console.log(moy);
	    var mymoy = L.geoJSON(moy, {color: 'green'}).addTo(map);
	});
};


// if (typeof mymoy !== "undefined"){
// 	var overlayMaps ={
// 	"moyenne": mymoy,
// 	"orginal":mymapdata
// 	}
// }
// else{
// 	var overlayMaps ={
// 	"orginal":mymapdata
// };
// }

// L.control.layers(null, overlayMaps).addTo(map);

$(window).on("beforeunload", function() {
	console.log("kflklkl");
 	fetch( "/leaving");
 	return 'coucou';
});