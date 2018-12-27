$(document).ready(function() {

    $(document).on('click','.attack', function() {

        //var attacker = $(this).attr('attacker');
        
        var attacker = $('#currentTurn').data();
        var action = $('#actionSelect option:selected').val();
        var target = $('#selectionList option:selected').val();
        var URL ="/attack"

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { attacker : attacker, action : action, target : target }
        });

        req.done(function(data) {

            $('#initiativeOrder').html(data);
            $("#fadetest").text(data.flavourText).fadeOut(3000);
        });
    });
});