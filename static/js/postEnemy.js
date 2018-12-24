$(document).ready(function() {

    $(document).on('click','.addEnemy', function() {

        var enemy = $('#enemySelect option:selected').val();
        var URL ="/"

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { enemy : enemy}
        });
    });

    $(document).on('click','.addHero', function() {

        var hero = $('#heroSelect option:selected').val();
        var URL ="/"
        var initiative = prompt("Please enter your Initiative Score", "");

        req = $.ajax({
            url : URL,
            type : 'POST',
            data : { hero : hero, initiative:initiative}
        });
    });

});