$(document).ready(function() {

    $(document).on('click','.attack', function() {

        var attacker = $(this).attr('attacker');
        var weapon = $('#weaponSelect option:selected').val();
        var target = $('#selectionList option:selected').val();

        req = $.ajax({
            url : '/attack',
            type : 'POST',
            data : { attacker : attacker, weapon : weapon, target : target }
        });
    });
});