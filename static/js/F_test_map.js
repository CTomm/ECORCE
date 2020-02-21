var map=L.map('map')

var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png' ;
var osmAttrib = 'Map data OpenStreetMap contributors' ;
var osm=new L.TileLayer(osmUrl, {attribution : osmAttrib}). addTo(map);
map.setView([45.9, 4.7 ], 9);





// geoJSON : Basic States Map
//L.geoJSON(commune_part20).addTo(map);

L.geoJSON(commune_part20,{
	style:style,
	onEachFeature : inter}	
).addTo(map);



//Adding Some Color pour les polygones :--------------

function getColor(d) {
    return d > 0.4  ? '#CBD2D0' :
           d > 0.3  ? '#CBD2D0' :
           d > 0.2  ? '#CBD2D0' :
           d > 0.1  ? '#CBD2D0' :
           d > 0    ? '#CBD2D0' :
                      '#CBD2D0';
}


function style(feature) {
    return {
        fillColor: getColor(feature.properties.part_20),
        weight: 1,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}
//--------------------





//interactions : -----------------------------------------

//Objetif 1:
//lorsque l’utilisateur clique sur une commune, 
//la care se centre et zoom sur cette commune

//Objetif 2:
//lorsque l’utilisateur clique sur une commune, 
//la care se centre et zoom sur cette commune. 
//+ la valeur de la part de -20 ans doit s’afficher dans la page HTML. 

// Quand on fait separement pour les 2 objetif :------------------------------------
// function inter (feature, Layer){
// 	Layer.on("click", function(){
// 		//objetif 1 :
// 		map.fitBounds(Layer.getBounds())
		

// 		//objetif 2 : 
// 		// var text  = feature.properties.nom + Math.round(feature.properties.part_20) ... pas noter
// 		// document.getElementById('part_20')

// 	})
// }
//---------------------------------------------------------------------------------------


//conbinner objetif d'interaction 1 et 2 : 

function inter (feature, Layer){
	Layer.on("click", function(ev){
		var bounds = ev.target.getBounds();		
		map.fitBounds(bounds);
    // var percentage = (feature.properties.part_20 * 100).toFixed(2);
		document.getElementById('part_20').innerHTML = ev.target.feature.properties.nom 
    // + " : " + percentage + "% de population qui a moins de 20 ans."
	});
}




//objetif d'interaction 3 : ----------------------------- pas arriver a faire

//<button onclick = "addMarker()" > Hasard</button>  @ Fichier HTML


// ajouter un point aleatoire:

// fonction addMarker ({})

// var bounds = map.getBounds();
// var x = bounds.getEast()+ Math.random() * (bounds.getWest() - bounds.getEast());
// var y = bounds.getSouth()+ Math.random() * (bounds.getNorth() - bounds.getSouth());
// L.marker([y,x]).addTo(map);























// Self - Essaye : Afficher des donnees - Gestionnaire de couches-----------

// var baseLayers = {
// 	"OpenStreetMap" : osm
// };

// var overlays = {
// 	"Commune de Lyon" : commune_part20
// };

// L.control.layers (baseLayers, overlays). addTo(map);

//-------------------









