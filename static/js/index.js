/*----------BOUTTONS ATTENTE---------------*/

document.getElementById("attente_moy").style.visibility='hidden'
document.getElementById("attente_id").style.visibility='hidden'
document.getElementById("attente_resend").style.visibility='hidden'

/*----------ONGLETS---------------*/

var anc_onglet = 'quoi';
change_onglet(anc_onglet);

function change_onglet(name){
    document.getElementById('onglet_' + anc_onglet).className = 'onglet_0 onglet';
    document.getElementById('onglet_' + name).className = 'onglet_1 onglet';
    document.getElementById('contenu_onglet_' + anc_onglet).style.display = 'none';
    document.getElementById('contenu_onglet_' + name).style.display = 'block';
    anc_onglet = name;
}

/*----------- MAP et position----------------*/

var locIcon = L.icon({
  iconUrl: 'image/marker.png',
  iconSize: [38, 38],
  iconAnchor: [19, 38]
  })


var positionsplit = localStorage.getItem("position").split(/ /);
var positioncenter = '[' +String(positionsplit[1]) + ', ' + String(positionsplit[0]) +']';

var map = L.map('map', {
    center: JSON.parse(positioncenter),
	zoomControl: false,
	minZoom: 0,
    maxZoom: 20,
    zoom: 12
});

//positionjs = L.geoJSON(JSON.parse(positioncenter)).addTo(map);
//console.log(JSON.parse(positioncenter));
L.marker(JSON.parse(positioncenter), {icon: locIcon}).addTo(map);;

//positioncenter(myLayerOptions

var StadiaAttib='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
var Stadia_AlidadeSmooth = new L.TileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png', {attribution: StadiaAttib}).addTo(map);

/*----------- STYLE ----------------*/

var styleideal = {
	"color": "#886176",
	"weight": 0.8, 
	"opacity": 0,
	"fillOpacity": 1
};  

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

var styleusercom = {
	weight: 3,
    color: '#666',
    dashArray: '',
    fillOpacity: 0.1
};

/*----------- LAYERS ----------------*/

var requetemoyenne = $.post( "/getemissionmoy", {
	position: localStorage.getItem('position')},
	function(consomoy) {
		CO2_moy = consomoy;
		var nom = consomoy.features[0].properties.nom;
		var hab = consomoy.features[0].properties.hab;
		localStorage.setItem("population", hab);
		var emission_moy = consomoy.features[0].properties.emission;
		var quartier = L.geoJSON(consomoy,{  // voir si c'est bon
											style:styleusercom,
											onEachFeature: function (feature,layer) {
											layer.bindPopup('<h5>'+nom+'</h5><p>Votre consommation a été multipliée par la population: '+hab+' habitants.</p>');
											}}).addTo(map);
		controlLayers.addOverlay(quartier, "<span style='color: black';'font:14px'>Votre quartier ou commune</span>") 

		// INFOS
		document.getElementById("em_moy").innerHTML =  Math.round(hab*5711.632476/10000)/100;
		document.getElementById("em_ideal").innerHTML =  Math.round(hab*1800/10000)/100;

		//GRAPHIQUE:
		myChart.config.data.datasets[0].data[2] = Math.round(emission_moy*0.4569/1000);
		myChart.config.data.datasets[1].data[2] = Math.round(emission_moy*0.2946/1000);
		myChart.config.data.datasets[2].data[2] = Math.round(emission_moy*0.2485/1000);
	});

var resultat = $.post( "/sendresultat", {
	position: localStorage.getItem('position')}, 
	function(parc) {
	    var conso_a = L.geoJSON(parc,{style:stylea}).addTo(map);
	    var distmax = parc.features[0].properties.maxdist;
	    var aire = parc.features[0].properties.aire;
	    var conso = parc.features[0].properties.total;
	    controlLayers.addOverlay(conso_a, "<span style='color: black';'font:14px'>Consommation actuelle</span>") 

		//INFOS;
		document.getElementById("surf").innerHTML = Math.round(aire/ 10000) ;
		document.getElementById("rayon").innerHTML =  Math.round(distmax/100)/10;
		document.getElementById("em_tot").innerHTML =  Math.round(conso/10000)/100;

		//GRAPHIQUE:
		myChart.config.data.datasets[0].data[0] = Math.round(localStorage.getItem('alim')*localStorage.getItem("population")/1000);
		myChart.config.data.datasets[1].data[0] = Math.round(localStorage.getItem('ener')*localStorage.getItem("population")/1000);
		myChart.config.data.datasets[2].data[0] = Math.round(localStorage.getItem('transp')*localStorage.getItem("population")/1000);
	});

$.when(resultat).done(function() {	
  	//console.log("I'm done");
  	var button = document.createElement("BUTTON");
	button.innerHTML = "Ok";
	button.setAttribute('type','button');
	button.setAttribute('id','simuFromBienvenue');
	button.setAttribute('class','sideButton button-simulation');
	button.onclick = function() {
		document.getElementById("volet_bienvenue").style.visibility='hidden'; document.getElementById("page").style.visibility='visible'
	}
	document.getElementById("div_button").appendChild(button);  
});

var isFirst = true;
function resend(){
	document.getElementById("attente_resend").style.visibility='visible'
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
      alim: localStorage.getItem('alim'),
      transport: localStorage.getItem('transp')
      },
      function(results) {
		var emissionindiv = results.emission;
		console.log(results);
		myChart.config.data.datasets[0].data[1] = Math.round(results.alim*localStorage.getItem("population")/1000);
		myChart.config.data.datasets[1].data[1] = Math.round(results.energie*localStorage.getItem("population")/1000);
		myChart.config.data.datasets[2].data[1] = Math.round(results.transport*localStorage.getItem("population")/1000);
		myChart.update();
		var change = $.post( "/getchangeresults", {
			position:localStorage.getItem('position'),
			emission:results.emission
		}, function(e) {
			var conso_b =L.geoJSON(e,{style:styleb})
			if (isFirst == false){
				test.remove();
				controlLayers.removeLayer(test);
			}
			test = conso_b.addTo(map);
			controlLayers.addOverlay(conso_b, "<span style='color: black';'font:14px'>Consommation modifiée</span>");
			isFirst = false;
		});
		$.when(change).done(function() {
			document.getElementById("attente_resend").style.visibility='hidden'
		});
		}
	);
	return false;
};

function moy(){
	document.getElementById("attente_moy").style.visibility='visible';
	var getmoyenne = $.post( "/sendmoyenne", {
	position: localStorage.getItem('position')},
	function(consomoy) {
		var distmax_moy = consomoy.features[0].properties.maxdist;
	    var aire_moy = consomoy.features[0].properties.aire;
	    var conso_moy = L.geoJSON(consomoy,{style:stylemoy}).addTo(map);
	    controlLayers.addOverlay(conso_moy, "<span style='color: black';'font:14px'>Consommation d'un français moyen</span>") 
	});
	$.when(getmoyenne).done(function() {
		document.getElementById("attente_moy").style.visibility='hidden';
	});
};

function sendideal(){
	document.getElementById("attente_id").style.visibility='visible';
	var getideal = $.post( "/sendideal", {
	position: localStorage.getItem('position')}, 
	function(parc) {
		console.log(parc);
	    var aire_ideal = parc.features[0].properties.aire;
	    var conso_ideal =  parc.features[0].properties.total;// 2 fois la variable 
	    var idealmap = L.geoJSON(parc,{style:styleideal}).addTo(map);
	    controlLayers.addOverlay(idealmap, "<span style='color: black';'font:14px'>Consommation optimale*</span>");
	    console.log("coucou");
	    document.getElementById("em_ideal").innerHTML =  Math.round(conso_ideal/10000)/100;
	$.when(getideal).done(function() {
		document.getElementById("attente_id").style.visibility='hidden';
	});
});
}

var commune = L.geoJSON(commune,
	{style:stylecom}).addTo(map);


/*----------- GESTION DES LAYERS-LEGENDE----------------*/

L.control.zoom({
     position:'topright'
}).addTo(map);


var overlays = {
	"<span style='color: black';'font:14px'>Communes, quartiers</span>": commune
}
var controlLayers = L.control.layers(null, overlays, {collapsed:false}).addTo(map);


var legend = L.control({ position: "bottomright" });

legend.onAdd = function(map) {
  var div = L.DomUtil.create("div", "legend");
  div.innerHTML += '<i style="background: #93A285"></i><span>Votre consommation</span><br>';
  div.innerHTML += '<i style="background: #004E2B"></i><span>Votre consommation modifiée</span><br>';
  div.innerHTML += '<i style="background: #D7833A"></i><span>Consommation comme un français "moyen"</span><br>';
  div.innerHTML += '<i style="background: #886176"></i><span>Consommation optimale*</span><br>';
  div.innerHTML += '<i class="icon" ></i><span>Votre adresse</span><br>';
  return div;
};
legend.addTo(map);

/*----------- INFOS ----------------*/



//Déplacé dans les fonctions où ces valeurs sont récupérées (sendresultat / sendmoyenne / sendideal)
// var surf = aire;
// document.getElementById("surf").innerHTML = surf;
// var rayon = distmax;
// document.getElementById("rayon").innerHTML = rayon;
// var em_tot = CO2_perso;
// document.getElementById("em_tot").innerHTML = em_tot;
// var em_moy = emission_moy;
// document.getElementById("em_moy").innerHTML = em_moy;
// var em_ideal = 72;
// document.getElementById("em_ideal").innerHTML = em_ideal;


/*----------- GRAPHIQUE ----------------*/


var ctx = document.getElementById('myChart').getContext('2d');
ctx.canvas.width = 30;
ctx.canvas.height = 24;

var alim_a = 0
var alim_b = 0

var ener_a = 0
var ener_b = 0

var transp_a = 0
var transp_b = 0


var myChartConfig = {
    type: 'bar',
    data: {
        labels: ["Vos émissions", "Vos émissions modifiées", "Emissions d'un français moyen"],
        datasets: [
           {
           label: "Alimentation",
           data: [0,0, 0],
		   backgroundColor: ['#93A285','#93A285','#93A285'],
           },{
           label: "Energie",
           data: [0,0,0],
		   backgroundColor: ['#004E2B','#004E2B','#004E2B']
           },{
           label: "Transport",
           data: [0,0,0],
		   backgroundColor: ['#D7833A','#D7833A','#D7833A'],
           }
        ]
    },
	options: {
		title: {
			display: true,
			text: 'Tonnes de dioxyde de carbone émis',
			fontColor: 'white'
        },
        scales: {
            xAxes: [{
                stacked: true,
                ticks: {
					fontColor: "white",
                    autoSkip: false,
                    maxRotation: 0,
                    minRotation: 0
                },
				labels: [["Vos", "émissions"], 
						["Vos", "émissions", "modifiées"],
						["Emissions", "d'un français", "moyen"]]
            }],
            yAxes: [{
                stacked: true
            }]
        },
		legend: {
            display: true,
            labels: {
                fontColor: 'white'
            }
        }
    }
}
var myChart = new Chart(ctx, myChartConfig);

/*----------- CLEARING WHEN USER LEAVING ----------------*/

$(window).on("beforeunload", function() {
 	fetch( "/leaving");
 	localStorage.clear();
});