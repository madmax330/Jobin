/**
 * Created by maxencecoulibaly on 11/4/16.
 */
$(function(){

    $('.warning-open').click(function(){
        var w = $('#bodyCol').width();
        var warn = $('.warning-container');
        warn.html($(this).siblings('.warning').html());
        warn.css('width', w+'px');
        warn.removeClass('hidden');
    });

    $('#bodyCol').on('click', '.warning-close', function(){
        $('.warning-container').addClass('hidden');
    });
});





