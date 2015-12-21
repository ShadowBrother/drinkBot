//admin.js
//Jesse Hoyt - jesselhoyt@gmail.com

//requires jquery

$(document).ready(function(){
    
    $('.flashes').fadeIn("slow").delay(500).fadeOut("slow");
    $('ul,li').disableSelection();
    $('#onHand').sortable();
    $('.slot, #remove').droppable({accept: '.liquid'});
    $('#onHand').droppable({accept: '.liquid' });
    $('.liquid').draggable({connectToSortable: "#onHand", snap: ".slot", snapMode: "inner", revert: 'invalid'});
    //$('.liquid').draggable();
    //$('.slot').droppable({drop: function(event, ui){alert("drop");alert($(event.target).find(".slot_number").html());ui.draggable.attr("slot_number", $(event.target).find(".slot_number").html())}});
    
});