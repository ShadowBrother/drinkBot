//drinkBot.js
//Jesse Hoyt - jesselhoyt@gmail.com

//requires jquery

//regular expressions for getting ingredient amount and name
amountRX =  /\d+\.?\d*/ ;
liquidNameRX = /\b[a-zA-Z]+\b/g

//flashes message
function flash(msg)
{
//FIX multiple flashings: make li's hidden and flashable as opposed to entire ul?
$newLi = $('<li>' + msg + '</li>') ;
//$newLi.appendTo('.flashes').fadeIn("slow").fadeOut("slow");
$('.flashes').append($newLi).fadeIn("800000").fadeOut("800000",function(){$newLi.remove();}) ;
}

//converts recipe elements to inputs
function recipeToInput(recipeForm)
{
    //alert("recipeToInput start");
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
    
    var drink = recipeForm.parent().prev()
    var drinkName = drink.text().trim();
    if(drinkName.indexOf("-") >= 0)//trim off -requires hand adding/-unavailable
        {
            drinkName = drinkName.substr(0, drinkName.indexOf("-")).trim() ;
        }
    recipeForm.prepend($('<input class="drinkName" name="drinkName" value="' + drinkName + '" hidden />'));//hidden input for drinkName in form
    drink.html($('<input class="drinkName" name="drinkName" value="' + drinkName + '" />'));//visible input for drinkName in h3
    
    for (i = 0; i < len; i++){
        $item = $(lis[i]);//make jquery object
        
        var text = $item.text().trim().replace(/[\n\r\t]/g,"").replace(/\s\s+/g, " ") ;//removes extra whitespace
        var amount =  amountRX.exec(text);//extract amount
        //alert(text);
        //alert(text.length);
        //alert("66.66 % Vermouth - Requires hand adding".length);
        //alert(text.indexOf("-"))
        if(text.indexOf("-") >= 0)//trim off -requires hand adding/-unavailable
        {
            text = text.substr(0, text.indexOf("-")) ;
        }
        var name = text.match(liquidNameRX) ;//extract liquid name
        var nameStr = "" ;
        for(j = 0, len2 = name.length; j < len2; j++)
        {
            nameStr += name[j] + " ";
        }
        //alert(liquidNameRX.test("dog"));
        //alert(liquidNameRX.test("dog cat"));
        //alert(liquidNameRX.test("12"));
        //alert(liquidNameRX.test("23 dog"));
        //alert(name);
        //alert($item.text().match(liquidNameRX)[1]);//get liquid Name
        $
        $newAmountInput = $('<input type="number" min="0" step="any" class="amount" name="amount" value="' + amount + '"/>');
        $newNameInput = $('<input name="name" type="text" value="' + nameStr + '" />');
        $item.html("");
        $item.append($newAmountInput);
        $item.append($newNameInput);
        $removeBtn = $('<button class="removeInputs" name="removeInputs" value="Remove">Remove</button>');//allow to remove ingredient
        $removeBtn.click(removeIngredient);
        $item.append($removeBtn);
    }
    //alert("recipeToInput end");
}

function removeIngredient(e)
{
    e.preventDefault();
    
    $(e.target).parent().remove();//remove the ingredient inputs
}

//adds inputs for new ingredient to be added
function addIngredient(e){

    e.preventDefault();
    //alert("Add New Ingredient");
    
    $newAmountInput = $('<input type="number" class="amount" name="amount" placeholder="0.0"></input>');
    $newNameInput = $('<input type="text" class="name" name="name" placeholder="Name of Ingredient"></input>');
    $removeBtn = $('<button class="removeInputs" name="removeInputs" value="Remove">Remove</button>');
    $removeBtn.click(removeIngredient);
    $ul = $(e.target).parent().find('ul');
    $li = $('<li/>');
    $li.append($newAmountInput);
    $li.append($newNameInput);
    $li.append($removeBtn);
    $ul.append($li);
}



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

//checks if order/save form is valid, returns true if valid and form should be submitted, false if not valid and form shouldn't be submitted
function validateForm(form)
{
    //alert("validateForm start");
    $form = $(form) ;
    
    var valid = true ;
    
    $drink = $form.parent().prev().find('input[name="drinkName"]') ;//drinkName input
    if($drink.val() == "")//check if empty
    {
        flash("Missing Drink Name", "error");
        valid = false;
    }
    else
    {
        //give hidden drinkName input the value of the visible drinkName input
        $form.find('input[name="drinkName"]').val($drink.val());
    }
    
    if($form.attr("action") == $form.attr("deleteURL"))//check if action is delete
    {
        return valid;//can return here since delete only cares if drinkName exists
    }
    
    if($form.find('li').length <= 0)
    {
        flash("No ingredients.", "error");
        return false;
    }
    //alert($form.find('input[name="name"]').length);
    var $nameInput = $form.find('input[name="name"]') ;
    for(i = 0, len = $nameInput.length; i < len; i++ )
    {
        //alert($($nameInput[i]).val());
        if($($nameInput[i]).val() == "")
        {
            flash("Missing Ingredient Name", "error");
            valid = false;
        }
    }
    
    var $amountInput = $form.find('input[name="amount"]');
    for(i = 0, len = $amountInput.length; i < len; i++)
    {
        if($($amountInput[i]).val() == "")
        {
            flash("Missing Ingredient Amount", "error");
            valid = false;
        }
    }
    
    
    //alert("validateForm end");
    return valid ;

}

function submitOrder(e){
        //alert("submitOrder start");
        $form = $(e.target).parent() ;
        $form.attr("action",$form.attr("orderURL"));
        
        recipeToInput($form);//converts recipe list to inputs
        //alert("submitOrder end");
        //return true ;
}

function saveRecipe(e)
{

    //alert("Saved but not really!") ;
    $form = $(e.target).parent() ;
    
    $form.attr("action",$form.attr("saveURL"));
   
}

function deleteDrink(e)
{

    //alert("Saved but not really!") ;
    $form = $(e.target).parent() ;
    
    $form.attr("action",$form.attr("deleteURL"));
    recipeToInput($form);//converts recipe list to inputs and more importantly creates drinkName input
}

$(document).ready(function(){

    //disable keyboard navigation of accordion since it doesn't play well with inputs
    $.ui.accordion.prototype._keydown = function(e){return;};
    
	$('#drinks').accordion();
	$('input.order').click(submitOrder);
    $('button#deleteDrink').click(deleteDrink);
    $('button.editOrder').click(function(e){
        e.preventDefault();
        $recipeForm = $(e.target).parent();//find Form
        recipeToInput($recipeForm);//converts recipe list to inputs
        //add button for adding additional ingredients
        $addIngredientBtn = $('<button class="addIngredient" name="addIngredient">Add New Ingredient</button>');
        $addIngredientBtn.click(addIngredient);
        $recipeForm.find('ul').after($addIngredientBtn);
        $(e.target).remove();
        isLoggedInMin( function(data){
            if(data.loggedIn){
                $saveButton = $('<input type="submit" id="saveEdit" name="saveEdit" class="saveEdit" value="Save" />');
                $saveButton.click(saveRecipe);
                $recipeForm.append($saveButton);
                //alert($recipeForm.attr("class"));
            }
        });
    });
    
    
    $('.flashes').fadeIn("800000").fadeOut("800000");
});