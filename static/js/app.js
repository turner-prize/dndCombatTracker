$(document).ready(function() {
    $(document).on('click','.nextItem', function() {
        $.get( "/nextItem", function( data ) {
            $('#mylist').html(data);
        });
    });
});