document.addEventListener('DOMContentLoaded', function(event) {
  showSlides(slideIndex);
});
var slideIndex = 1;
// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  //dots[slideIndex-1].className += " active";
}

//Récupération des valeur pour le Et si :

// try {
//   // console.log("hello")
//   // var poulet =  parseFloat(document.getElementById("poulet").options[ document.getElementById("poulet").selectedIndex].value);
//   // var porc =   parseFloat(document.getElementById("porc").options[ document.getElementById("porc").selectedIndex].value);
//   // var agneau =   parseFloat(document.getElementById("agneau").options[ document.getElementById("agneau").selectedIndex].value);
//   // var boeuf =   parseFloat(document.getElementById("boeuf").options[ document.getElementById("boeuf").selectedIndex].value);
//   // viande = poulet+porc+agneau+boeuf
//   // console.log(viande)
//   // localStorage.setItem('viande', viande);
//   console.log(document.getElementById("Q7b-A").checked);
// }
// catch(err) {
//   console.log(err);
// };

// function avion(){
//   var energie = 0;
//   var energie = energie + parseFloat(document.getElementById("Q9-A").value) + parseFloat(document.getElementById("Q9-B").value) +parseFloat(document.getElementById("Q9-C").value)+parseFloat(document.getElementById("Q9-D").value);
//   console.log(energie);
// }

function keepresults(){
  try {
  var  poulet =  214.4*parseFloat(document.getElementById("poulet").options[ document.getElementById("poulet").selectedIndex].value);
  var porc =   304.2*parseFloat(document.getElementById("porc").options[ document.getElementById("porc").selectedIndex].value);
  var agneau =   1451.32*parseFloat(document.getElementById("agneau").options[ document.getElementById("agneau").selectedIndex].value);
  var boeuf =   1493.96*parseFloat(document.getElementById("boeuf").options[ document.getElementById("boeuf").selectedIndex].value);
  console.log(poulet + '' + porc+ '' + agneau+ '' + boeuf);
    if (document.getElementById("Q4-A").checked == true){
      var poisson = 0
    }
    else if (document.getElementById("Q4-B").checked == true){
      var poisson = 22.78607013*1.5
    }
    else if (document.getElementById("Q4-C").checked == true){
      var poisson = 22.78607013*3.5
    }
    else if (document.getElementById("Q4-D").checked == true){
      var poisson = 22.78607013*7
    }
    else if (document.getElementById("Q4-E").checked == true){
      var poisson = 22.78607013*14
    }
  viande = poulet+porc+agneau+boeuf+poisson;
  console.log(viande);
  localStorage.setItem('viande', viande);
  }
  catch(err) {
    console.log(err);
  };
  var avion = parseFloat(document.getElementById("Q17-A").value);
  localStorage.setItem('avion', avion);
  var voiture = parseFloat(document.getElementById("Q13-A").value);
  localStorage.setItem('voiture', voiture);

  var energie = parseFloat(document.getElementById("Q9-A").value)*12 + parseFloat(document.getElementById("Q9-B").value)*11.53 +parseFloat(document.getElementById("Q9-C").value)*1.289+parseFloat(document.getElementById("Q9-D").value)*1.5;
  localStorage.setItem('energie', energie)

  if (document.getElementById("Q7b-A").checked == true){
    localStorage.setItem('legume', 1.02284)
  }
  else if (document.getElementById("Q7b-B").checked == true){
    localStorage.setItem('legume',0.17108)
  }
}