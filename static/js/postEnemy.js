$(document).ready(function() {

    $(document).on('click','.add', function() {

        var enemy = $('#enemySelect option:selected').val();
        var URL ="/"

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { enemy : enemy}
        });

    });
});