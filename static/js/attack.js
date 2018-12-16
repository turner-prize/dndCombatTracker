$(document).ready(function() {

    $(document).on('click','.attack', function() {

        var attacker = $(this).attr('attacker');

        var name = $('#nameInput'+member_id).val();
        var email = $('#emailInput'+member_id).val();

        req = $.ajax({
            url : '/update',
            type : 'POST',
            data : { name : name, email : email, id : member_id }
        });

        req.done(function(data) {

            $('#memberSection'+member_id).fadeOut(1000).fadeIn(1000);
            $('#memberNumber'+member_id).text(data.member_num);

        });
    

    });

});