$(document).ready(function() {
    $(document).on('click','.nextItem', function() {
        $.get( "/nextItem", function( data ) {
            $('#initiativeOrder').html(data);
            //$('#currentTurn').text(data.nextitem);
        });
    });
});