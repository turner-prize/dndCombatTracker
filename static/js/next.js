  $('#nextButton').on('click', function(){
    $.get( "/nextItem", function( data ) { 
        $("#initiativeOrder").html(data);
        });    
    });
    
