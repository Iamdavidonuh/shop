
$(document).ready(function(){
	//get item price
	var get_price = parseInt($(".item-price{{items.id}}").text());
	//set item total
	var set_price = $(".item-total{{items.id}}").text(get_price);
	
	//get item_total
	var item_total = parseInt(set_price.text());
	var quantity
	$(document).on('blur','#qty{{items.id }}', function(){
		quantity =parseInt($("#qty{{items.id}}").val());
		//add loading class here
		//get total price of individual of item product here
		$.ajax({
			url:"{{url_for('users.quantity_update',id = items.id)}}",
			type:"POST",
			data: {quantity:quantity}
		});
		//remove loading class here
		set_price = $(".item-total{{items.id}}").text(quantity*item_total).fadeOut(100).fadeIn(1000);
		$("#qty{{items.id}}").fadeOut(1000).fadeIn(1000);
		
	});
})

