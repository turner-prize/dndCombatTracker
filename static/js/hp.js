$(document).ready(function() {

    $(document).on('click','.attack', function() {

        var attacker = $(this).attr('attacker');
        var action = $('#actionSelect option:selected').val();
        var target = $('#selectionList option:selected').val();
        var URL ="/attack2"

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { attacker : attacker, action : action, target : target }
        });

        req.done(function(data) {

            $('#result').text(data.result);

        });
    });
});