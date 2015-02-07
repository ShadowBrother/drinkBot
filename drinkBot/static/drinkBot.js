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
function recipeToInput($recipeForm)
{
    //alert("recipeToInput start");
    if($recipeForm.find('input[name="amountOz"]').length > 0)
    {
        //alert(recipeForm.find('input[name="amount"]').length);
        //alert("already input") ;
        return; //recipe has already been turned to input
    }
    //alert(recipeForm.find('input'[name="amount"]).length);
    
    //alert($(recipeForm.find('li')[0]).text());
    var lis = $recipeForm.find('li');
    var len = lis.length;
    
    var drink = $recipeForm.parent().prev()
    var drinkName = drink.text().trim();
    if(drinkName.indexOf("-") >= 0)//trim off -requires hand adding/-unavailable
        {
            drinkName = drinkName.substr(0, drinkName.indexOf("-")).trim() ;
        }
    $recipeForm.prepend($('<input class="drinkName" name="drinkName" value="' + drinkName + '" hidden />'));//hidden input for drinkName in form
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
        for(j = 1, len2 = name.length; j < len2; j++)//j = 1 to ignore "oz"
        {
            nameStr += name[j] + " ";
        }
        //alert(liquidNameRX.test("dog"));
        //alert(liquidNameRX.test("dog cat"));
        //alert(liquidNameRX.test("12"));
        //alert(liquidNameRX.test("23 dog"));
        //alert(name);
        //alert($item.text().match(liquidNameRX)[1]);//get liquid Name
        
        $newAmountInput = $('<input type="number" min="0" step="any" class="amount oz" name="amountOz" value="' + amount + '" />'); //'" onchange="updateTotal($(this).parent().parent().parent())"/>');
        $newAmountPercentInput = $('<input type="number" min="0" step="any" class="amount percent" name="amountPercent" value="' + ozToPercent(parseFloat($recipeForm.find(".glassSize").val()), amount) + '" />');
		//alert($recipeForm.find(".glassSize").val());
		
		
		
		//glassSize probably needs a separate, default onChange handler for when it's not in editing mode
		//to change the displayed recipe. Would require turning on/off the 2 handlers.
		$recipeForm.find(".glassSize").change(updatePercent) ;//if glassSize changes, the percentages need to change.
		$newNameInput = $('<input name="name" type="text" value="' + nameStr + '" />');
		
		//add update handlers to amount inputs
		$newAmountInput.change(updatePercent).keypress(disableEnter);
		$newAmountPercentInput.change(updateOz).keypress(disableEnter);
		$newNameInput.keypress(disableEnter);
        
		$item.html("");
        $item.append($newAmountInput);
		$item.append($('<span>oz</span>'));
		$item.append($newAmountPercentInput);
		$item.append($('<span>%</span>'));
        $item.append($newNameInput);
        $removeBtn = $('<button class="removeInputs" name="removeInputs" value="Remove">Remove</button>');//allow to remove ingredient
        $removeBtn.click(removeIngredient);
        $item.append($removeBtn);
    }
    //alert("recipeToInput end");
}

//disableEnter in inputs to stop from accidentally deleting input
function disableEnter(e)
{

	if (e.keyCode == 10 || e.keyCode == 13) 
        e.preventDefault();
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
    
	//add inputs for new ingredient
    $newAmountInput = $('<input type="number" class="amount oz" name="amountOz" placeholder="0.0"></input>');
	$newAmountPercentInput = $('<input type="number" class="amount percent" name="amountPercent" placeholder="0.0"></input>');
    $newNameInput = $('<input type="text" class="name" name="name" placeholder="Name of Ingredient"></input>');
    $removeBtn = $('<button class="removeInputs" name="removeInputs" value="Remove">Remove</button>');
    //add handlers to buttons/inputs
	$removeBtn.click(removeIngredient);
	$newAmountInput.change(updatePercent).keypress(disableEnter);
	$newAmountPercentInput.change(updateOz).keypress(disableEnter);
	$newNameInput.keypress(disableEnter);
	
    //find ingredient list
	$ul = $(e.target).parent().find('ul');
    $li = $('<li/>');
	//append ingredient inputs/buttons to ingredient list
    $li.append($newAmountInput);
	$li.append($newAmountPercentInput);
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
    
    var $amountInput = $form.find('input[name="amountOz"]');
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


//totals amount of all ingredients
//returns float of total
//recipeForm (jQuery object) : Form containing recipe elements
function total($recipeForm)
{

	var total = 0.0 ;
	var $lis = $recipeForm.find('li')
	for(i = 0, len = $lis.length; i < len ; i++)
	{
		total += parseFloat($($lis[i]).find('.amount.percent').val()) ;
	}
	return total ;
}

//update total when amount input changed
function updateTotal(e){

	var $recipeForm = $(e.target).parent().parent().parent() ;
	var totl = total($recipeForm) ;
	$recipeForm.find('.total').val(totl) ;
	if((totl > 100) || (totl <= 0))//if total is out of range error message
	{
	
		$recipeForm.find('.totalError').html("Where'd you learn to math?") ;
	
	}
	else//if no error, clear any error message that might be there
	{
		$recipeForm.find('.totalError').html("") ;
	}
}

//update percent input when oz is changed
function updatePercent(e)
{
	var $amountInput = $(e.target) ;
	var $recipeForm = $amountInput.parent().parent().parent() ;
	$percentInput = $amountInput.siblings(".percent") ;
	newPercentValue = ozToPercent(parseFloat($recipeForm.find(".glassSize").val()), parseFloat($amountInput.val())) ;//calculate new percentage
	if(parseFloat($percentInput.val()) != newPercentValue)//avoid infinite loop of updating percent and oz inputs
		{
		$percentInput.val(newPercentValue) ;//update percent value
		}
	updateTotal(e) ;
}

//update oz input when amount is changed
function updateOz(e)
{
	var $percentInput = $(e.target) ;
	var $recipeForm = $percentInput.parent().parent().parent() ;
	$ozInput = $percentInput.siblings(".oz") ;
	newOzValue = percentToOz(parseFloat($recipeForm.find(".glassSize").val()), parseFloat($percentInput.val()))  ;//calculate new percentage
	if(parseFloat($ozInput.val()) != newOzValue)//avoid infinite loop of updating percent and oz inputs
		{
		$ozInput.val(newOzValue) ;//update percent value
		}
	updateTotal(e) ;
	

}

function ozToPercent(glassSizeOz, oz){

	return oz / glassSizeOz * 100 ;
}

function percentToOz(glassSizeOz, percent){

	return percent / 100 * glassSizeOz ;

}
//editOrder click handler, converts recipe to allow editing
function editOrder(e)
{
        e.preventDefault();
        $recipeForm = $(e.target).parent();//find Form
        recipeToInput($recipeForm);//converts recipe list to inputs
		//total percent so can't go over
		var totl = total($recipeForm) ;
		$total = $('<input type="number" min="0" max="100" name="total" class="total" value="' + totl + '" readonly />');
		$totalError = $('<div class="totalErrorDiv"><p name="totalError" class="totalError error"></p></div>');
		$total.keypress(disableEnter);
		
        //add button for adding additional ingredients
        $addIngredientBtn = $('<button class="addIngredient" name="addIngredient">Add New Ingredient</button>');
        $addIngredientBtn.click(addIngredient);
		//append addIngredientBtn, TotalError, and total after ul
        $recipeForm.find('ul').after($addIngredientBtn);
        $recipeForm.find('ul').after($totalError);
		$recipeForm.find('ul').after($total);
		
		$(e.target).remove();
        isLoggedInMin( function(data){
            if(data.loggedIn){
                $saveButton = $('<input type="submit" id="saveEdit" name="saveEdit" class="saveEdit" value="Save" />');
                $saveButton.click(saveRecipe);
                $recipeForm.append($saveButton);
                //alert($recipeForm.attr("class"));
            }
        });
}

$(document).ready(function(){

    //disable keyboard navigation of accordion since it doesn't play well with inputs
    $.ui.accordion.prototype._keydown = function(e){return;};
    
	$('#drinks').accordion();
	$('input.order').click(submitOrder);
    $('button#deleteDrink').click(deleteDrink);
    $('button.editOrder').click(editOrder);
    
    
    $('.flashes').fadeIn("800000").fadeOut("800000");
});