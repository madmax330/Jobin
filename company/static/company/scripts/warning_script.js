/**
 * Created by maxencecoulibaly on 5/14/17.
 */

/*
*
*   WARNINGS
*
*/


$(function(){

    $('.warning-open').click(function(){
        let warn = $('#warning-'+$(this).data('id'));
        let modal = $('#warning-modal');
        warn.find('.name').html($(this).data('name'));
        modal.find('.warning-message').html(warn.find('.message').html());
        modal.find('.warning-note').html(warn.find('.note').html());
        modal.find('.warning-accepted').attr('data-url', $(this).data('url'));
        modal.modal('toggle');
    });

    $('.warning-accepted').click(function(){
        send_get($(this).data('url'));
    });

});





