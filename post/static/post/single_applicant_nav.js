/**
 * Created by maxencecoulibaly on 2/14/17.
 */



$(function(){

    $('.single-app-view').click(function(){

        var form = $('#single-view-form');
        var url = $(this).data('url');

        var maj = $('#single-majors');
        var sch = $('#single-schools');

        maj.val(maj.val().substring(0,maj.val().length-1));
        sch.val(sch.val().substring(0,sch.val().length-1));

        form.attr('action', url);
        form.submit();

    });

    $('.multiple-app-view').click(function(){

        var form = $('#multiple-view-form');
        var url = $(this).data('url');

        var schools = $('#multi-schools');
        var majors = $('#multi-majors');

        schools.val(schools.val().substring(0,schools.val().length-1));
        majors.val(majors.val().substring(0,majors.val().length-1));

        form.attr('action', url);
        form.submit();

    });

});






