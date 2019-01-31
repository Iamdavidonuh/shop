$(document).ready(function(){
	$(document).on('blur','#qty{{items.id }}', function(){
		var quantity =parseInt($("#qty{{items.id}}").val());
		$.ajax({
			url:"http://localhost:5000/cart/update/1",
			//url:"{{url_for('users.quantity_update',id = items.id)}}",
			type:"POST",
			data: {quantity:quantity}
		});
		$("#qty{{items.id}}").fadeOut(1000).fadeIn(1000);
	});
})