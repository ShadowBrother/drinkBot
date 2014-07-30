//drinkBot.js
//Jesse Hoyt - jesselhoyt@gmail.com

//requires jquery

//regular expressions for getting ingredient amount and name
amountRX =  /\d+\.?\d*/ ;
liquidNameRX = /\d+\.?\d* % (\w+)/;

//flashes message
function flash(msg)
{

$('.flashes').append('<li>' + msg + '</li>').fadeIn("slow").fadeOut("slow");

}

//converts recipe elements to inputs
function recipeToInput(recipeForm)
{
    if(recipeForm.find('input[name="amount"]').length > 0)
    {
        //alert(recipeForm.find('input[name="amount"]').length);
        //alert("already input") ;
        return; //recipe has already been turned to input
    }
    //alert(recipeForm.find('input'[name="amount"]).length);
    
    //alert($(recipeForm.find('li')[0]).text());
    var lis = recipeForm.find('li');
    var len = lis.length;
    for (i = 0; i < len; i++){
        $item = $(lis[i]);//make jquery object
        amount =  amountRX.exec($item.text());
        name = liquidNameRX.exec($item.text())[1];
        //alert(name);
        //alert($item.text().match(liquidNameRX)[1]);//get liquid Name
        $newAmountInput = $('<input type="number" min="0" step="any" class="amount" name="amount" value="' + amount + '"></input>');
        $newNameLabel = $('<input name="name" type="text" value="' + name + '" />');
        $item.html("");
        $item.append($newAmountInput);
        $item.append($newNameLabel);
    }
    
}

//adds inputs for new ingredient to be added
function addIngredient(e){

    e.preventDefault();
    //alert("Add New Ingredient");
    alert(amountRX.toString());
    alert(amountRX.test(50.0));
    $newAmountInput = $('<input type="number" class="amount" name="amount" placeholder="0.0"></input>');
    $newNameInput = $('<input type="text" class="name" name="name" placeholder="Name of Ingredient"></input>');
    $ul = $(e.target).parent().find('ul');
    $li = $('<li/>');
    $li.append($newAmountInput);
    $li.append($newNameInput);
    $ul.append($li);
}

//AJAX checks if logged in and does callback
//args (dict of key-value pairs) : arguments to be passed to callback. ex: {key: "value", key2: 9"}
//callback (function) : function to call upon response, should have arguments args(if you plan on passing it args)
// and data(JSON with loggedIn set to true or false by server side code)


//checks if user is currently logged in
//returns JSON object with either true or false named field and a description string as value
//onTrue (function) : function to call if user logged in
//tArg (?) : argument to call onTrue with
//onFalse (function) : function to call if user is not logged in
//fArg (?) : argument to call onFalse with

function isLoggedIn(onTrue,tArg, onFalse, fArg){

	$.ajax({
		type: "GET",
		url: "/flask/db/_isLoggedIn",
		dataType: "json",
		error: function(XMLHttpRequest, textStatus, errorThrown){
				flash('responseText: ' + XMLHttpRequest.responseText);
                flash('textStatus: ' + textStatus );
                flash('errorThrown: ' + errorThrown );					
          		
		},
		//data contains JSON values returned by perl script
		//true or false named fields, with description string as value
		success: function(data){
			if(data.true){
				//alert(data.true) ;
				//alert(tArg) ;
				onTrue(tArg,data) ;
			}
			else{
				//alert(data.false) ;
				onFalse(fArg,data) ;
			}
		}//success
	});//ajax
}

//like isLoggedIn but only takes one callback function that will run whether logged in or not and expects no extra arguments
function isLoggedInMin(callback)
{
    $.getJSON("/flask/db/_isLoggedIn",{}, callback);    

}

function submitOrder(form){
        $recipeForm = $(form);//find Form
        recipeToInput($recipeForm);//converts recipe list to inputs
        return true ;
}

$(document).ready(function(){

	$('#drinks').accordion();
	$('button.order').click(function(e){
		e.preventDefault();
        alert('You ordered drink: ' + $(e.target).attr('id')) ;
	});
    $('button.editOrder').click(function(e){
        e.preventDefault();
        $recipeForm = $(e.target).parent().parent();//find Form
        recipeToInput($recipeForm);//converts recipe list to inputs
        //add button for adding additional ingredients
        $addIngredientBtn = $('<button class="addIngredient" name="addIngredient">Add New Ingredient</button>');
        $addIngredientBtn.click(addIngredient);
        $recipeForm.find('ul').after($addIngredientBtn);
        $(e.target).remove();
        isLoggedInMin( function(data){
            if(data.loggedIn){
                $saveButton = $('<button id="saveEdit" name="saveEdit" class="saveEdit">Save</button>');
                $saveButton.click(function(){flash("Saved! but not really");});
                $recipeForm.append($saveButton);
            }
        });
    });
    
    
    $('.flashes').fadeIn("slow").fadeOut("slow");
});