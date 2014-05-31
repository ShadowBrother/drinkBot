//drinkBot.js
//Jesse Hoyt - jesselhoyt@gmail.com

//requires jquery

$(document).ready(function(){

	$('#drinks').accordion();
	$('button.order').click(function(e){
		alert('You ordered drink: ' + $(e.target).attr('id')) ;
	});
});