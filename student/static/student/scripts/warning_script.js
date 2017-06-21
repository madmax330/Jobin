/**
 * Created by maxencecoulibaly on 5/7/17.
 */



$(function(){

    $('.warning-open').click(function(){
        let modal = $('#warning-modal');
        let warning = $('#warning-'+$(this).data('id'));
        warning.find('.name').html($(this).data('name'));
        modal.find('.warning-message').html(warning.find('.message').html());
        modal.find('.warning-notes').html(warning.find('.notes').html());
        modal.find('.warning-accepted').attr('data-url', $(this).data('url'));
        open_modal('warning-modal');
    });

    $('.warning-accepted').click(function(){
        send_get($(this).data('url'));
        close_modal('warning-modal');
    });

});

