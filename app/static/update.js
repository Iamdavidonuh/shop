
window.onload = initPage;

function initPage(){
	
	document.getElementById('qty1').onblur = changeQuantityReq;

	document.getElementsByClassName('checkoutcontainer').disabled = true;
}

function changeQuantityReq(){
	document.getElementById('loading').className = 'loading';
	// create a request object and send it to the server
	request = createRequest()

	if (request == null){
		return;
	}
	else{
		var input_value = document.getElementById('qty1').value;
		var quantity = escape(input_value);
	
		var url= "http://127.0.0.1:5000/cart/update/1"
		request.open("POST", url, true);
		request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		request.onreadystatechange = changeQty;
		request.send("quantity="+quantity);

	}
}

function changeQty(){
	if(request.readyState == 4){
		if(request.status == 200){
			if (request.responseText == "okay") {
				document.getElementById('loading').className = ''
				document.getElementsByClassName('checkoutcontainer').disabled = false;
			}
		}
	}
}