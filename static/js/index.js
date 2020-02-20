
var map = L.map('map');

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';

var osmAttrib='Map data by OpenStreetMap contributors';
map.setView([45.75, 4.8], 11);
var osm = new L.TileLayer(osmUrl, {attribution: osmAttrib}).addTo(map);

$.get( "/sendresultat", function(parc) {
	console.log(parc);
    var mymapdata = L.geoJSON(parc).addTo(map);
});


// Récupérer les valeurs du formulaire
$.get( "/change", function(emission) {
	console.log(emission);
    //document.getElementById("Q9-A").value = parseInt(viande)
});
// $.get( "/legume", function(legume) {
// 	console.log('legume'+legume);
// 	new_legume= legume
//     //document.getElementById("Q9-A").value = parseInt(legume)
// });
// $.get( "/avion", function(avion) {
// 	console.log('avion'+avion);
// 	new_avion = avion
//     //document.getElementById("Q9-A").value = parseInt(avion)
// });
// $.get( "/voiture", function(voiture) {
// 	console.log('voiture'+voiture);
// 	new_voiture = voiture
//     //document.getElementById("Q9-A").value = parseInt(voiture)
// });
// $.get( "/energie", function(energie) {
// 	console.log('energie'+energie);
// 	new_energie = energie
//     //document.getElementById("Q9-A").value = parseInt(energie)
// });
// $.get( "/emission", function(emission) {
// 	console.log('emissions'+emission);
// 	new_emission = emission
//     //document.getElementById("Q9-A").value = parseInt(emission)
// });

function resend(){
    $.post( "/sendresultat", {
      emission:emission
      })
};

function show(){
	$.get( "/sendmoyenne", function(moy) {
		console.log(moy);
	    var mymoy = L.geoJSON(moy, {color: 'red'}).addTo(map);
	});
}

