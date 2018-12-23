$(document).ready(function() {
    $(document).on('click','.nextItem', function(){        
        $.get( "/nextItem", function( data ) {            
            $('#initiativeOrder').html(data);        
        });    
    });
});