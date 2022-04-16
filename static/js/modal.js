const modal = document.getElementById('myModal');

const span = document.getElementsByClassName('close')[0];

span.onclick = () => {
	modal.style.display = 'none';
}

window.onclick = (e) => {
	if(e.target == modal){
		modal.style.display = 'none';
	}
}

function openModal(){
	modal.style.display = 'block';
}