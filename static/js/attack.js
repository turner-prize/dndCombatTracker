$(document).ready(function() {

    $(document).on('click','.attack', function() {

        var attacker = $(this).attr('attacker');
        var weapon = $('#weaponSelect option:selected').val();
        var target = $('#selectionList option:selected').val();
        var URL ="/attack"

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { attacker : attacker, weapon : weapon, target : target }
        });

        req.done(function(data) {

            $('#update').html(data);

        });
    });
});