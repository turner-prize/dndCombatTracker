$(document).ready(function() {
    $(document).on('click','.nextItem', function() {
        $.get( "/nextItem", function( data ) {
            $('#update').html(data);
        });
    });
});