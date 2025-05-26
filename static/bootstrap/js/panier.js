	liste = document.getElementsByClassName('active');
function addcart(){
	let item = {}
	if ( liste.length < 6){
		item = {
			nom : document.getElementById("item_name").textContent,
			price : document.getElementById("item_price").textContent,
			image : Image,
			size : SIZE,
			quantite : document.getElementById("valeurQuantite").value,
		};
	}else{
		item = {
			nom : document.getElementById("item_name").textContent,
			price : document.getElementById("item_price").textContent,
			image : Image,
			Ram : RAM,
			Rom : ROM,
			So : SO,
			Processeur : PROCESSEUR,
			Screen : SCREEN,
			quantite : document.getElementById("valeurQuantite").value,
		};
	}
	console.log(item)
	if(!localStorage.getItem(item.nom)){
		localStorage.setItem(item.nom, JSON.stringify(item));
		}else{

		};
	let total = 0;
	for (var i = 1 ; i <= localStorage.length; i++) {
		total += i ;
	}
	document.getElementById("PANIER").innerHTML = total;
};
