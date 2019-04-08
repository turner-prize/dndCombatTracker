$('#manualDamage').on('click', function() {
        
    var attacker = $('#currentTurn').data();
    var target = $('#targetSelect option:selected').val();
    var URL ="/manualDamage"
    var damage = prompt("Enter damage amount:", "");

    req = $.ajax({
        url : URL,
        type : 'POST',
        data : { attacker : attacker, target : target, damage: damage }
    });

    req.done(function(data) {
        $('#initiativeOrder').html(data);
        $('#fadeTest').fadeOut(5000);
    });
});
