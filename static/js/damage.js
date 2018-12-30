$(document).ready(function() {

    $(document).on('click','.damage', function() {
        
        var attacker = $('#currentTurn').data();
        var target = $('#selectionList option:selected').val();
        var URL ="/manualDamage"
        var damage = prompt("Enter damage amount:", "");

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { attacker : attacker, target : target, damage: damage }
        });

        req.done(function(data) {

            $('#initiativeOrder').html(data);
            // $("#fadetest").text(data.flavourText).fadeOut(3000);
        });
    });
});