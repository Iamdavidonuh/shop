function createRequest(){
	try{
		request = new XMLHttpRequest();
	}catch(tryMs){
		try{
			request = new ActiveXObject('ms12.XMLHTTP');
		}catch(otherMs){
			try{
				request = new ActiveXObject('Microsoft.XMLHTTP');
			}catch(failed){
				request = null;
			}
		}
	}
	return request;
}

//var url= "{{url_for('users.quantity_update', id=cart_item.id)}}"