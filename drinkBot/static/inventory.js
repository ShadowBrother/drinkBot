//admin.js
//Jesse Hoyt - jesselhoyt@gmail.com

//requires jquery

$(document).ready(function(){
    
    $('.flashes').fadeIn("slow").delay(500).fadeOut("slow");
    $('ul,li').disableSelection();
    $('#onHand').sortable({/*receive: function(e, ui)
        {
            alert("dropped in onHand");
            lis = $(this).find('li') ;
            alert(lis.length);
            for(i = 0, len = lis.length; i < len; ++i)//go through li's to see if empty one to put liquid span in
                {
                    alert($(lis[i]).find('span').length);
                    if($(lis[i]).find('span').length  <= 0)//an empty slot li
                        {
                            lis[i].append(ui.item);//append dragged .liquid span to .slot li
                            alert(lis[i]);
                            return;
                        }
                }
            alert("no empty li found, creating new one");
            //no empty li was found, create new one to put .liquid span in
            $newLi = $('<li class="slot"/>');
            alert(ui.item.html());
            //$newLi.append($(ui.item));
            //$(this).append($newLi);
            ui.item.wrap($newLi);
            return ;
        }*/});
    $('.slot, #remove').droppable({accept: '.liquid', drop: function(e, ui){
        
        alert("dropped");
        
        //grab ID of ui.draggable object
        
        //Destroy sortable and release all event handlers
        $('#onHand').sortable("destroy");
        
        //Append the JQuery object
        ui.draggable.appendTo($(this));
        
        //reset sortable
        $('#onHand').sortable();
    }
        
    });
    //$('#onHand').droppable({accept: '.liquid' });
    $('.liquid').draggable({connectToSortable: "#onHand", snap: ".slot", snapMode: "inner", revert: 'invalid', containment: 'window'});
    //$('.liquid').draggable();
    //$('.slot').droppable({drop: function(event, ui){alert("drop");alert($(event.target).find(".slot_number").html());ui.draggable.attr("slot_number", $(event.target).find(".slot_number").html())}});
    $('#lists, #onHand, #inBot').disableSelection();
});