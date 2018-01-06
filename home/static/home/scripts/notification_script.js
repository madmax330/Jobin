/**
 * Created by maxencecoulibaly on 12/7/16.
 */

$(function(){

    $('#close-all-notes').click(function(){
        send_get($(this).data('url'));
    });

    $('.close-note').click(function(){
        send_get($(this).data('url'));
    });

});

