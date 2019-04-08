$('#attackButton').on('click', function() {

    //var attacker = $(this).attr('attacker');
    
    var attacker = $('#currentTurn').data();
    var action = $('#actionSelect option:selected').val();
    var target = $('#targetSelect option:selected').val();
    var URL ="/attack"

    req = $.ajax({
        url : URL,
        type : 'POST',
        data : { attacker : attacker, action : action, target : target }
    });

    req.done(function(data) {
        $('#initiativeOrder').html(data);
        $('#fadeTest').fadeOut(5000);
    });
});


//https://stackoverflow.com/questions/27917471/pass-parameter-with-python-flask-in-external-javascript
//https://stackoverflow.com/questions/11178426/how-can-i-pass-data-from-flask-to-javascript-in-a-template