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
        let redirect = $(this).data('redirect');
        warn.find('.name').html($(this).data('name'));
        modal.find('.warning-message').html(warn.find('.message').html());
        modal.find('.warning-note').html(warn.find('.note').html());
        modal.find('.warning-accepted').attr('data-url', $(this).data('url'));
        if(redirect)
            modal.find('.warning-accepted').attr('data-redirect', redirect);
        modal.modal('toggle');
    });

    $('.warning-accepted').click(function(){
        let redirect = $(this).data('redirect');
        let url = $(this).data('url');
        $.get(url, function(data, status){

            if(status === 'success'){
                if(redirect)
                    window.location = redirect;
                else
                    location.reload();
            }

        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    });

});





