/**
 * Created by maxencecoulibaly on 6/1/17.
 */



$(function(){

    $('#suggestion-form').submit(function( event ) {
         event.preventDefault();

         send_post($(this).attr('action'), $(this));

    });

    $('.suggestion-comment').click(function(){
        let parent = $(this).parents('.jobin-suggestion');
        let modal = $('#suggestion-comment-modal');
        modal.find('.suggestion').html(parent.find('.suggestion').html().toString().trim());
        $('#suggestion-form').attr('action', $(this).data('url'));
        modal.modal('toggle');
    });

    $('#comment-form').submit(function ( event ) {
        event.preventDefault();

        send_post($(this).attr('action'), $(this));

    });

});




