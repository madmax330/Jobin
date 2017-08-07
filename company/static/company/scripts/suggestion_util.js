/**
 * Created by maxencecoulibaly on 6/1/17.
 */



$(function(){

    $('.view-suggestion').click(function ( event ) {
        event.preventDefault();

        let parent = $(this).parents('.jobin-suggestion');
        let modal = $('#suggestion-info-modal');

        modal.find('.suggestion-info-date').html(parent.find('.date').html().toString().trim());
        modal.find('.suggestion-info-topic').html(parent.find('.topic').html().toString().trim());
        modal.find('.suggestion-info-suggestion').html(parent.find('.suggestion').html().toString().trim());
        modal.modal('toggle');
    });

    $('#suggestion-form').submit(function( event ) {
         event.preventDefault();

         send_post($(this).attr('action'), $(this));

    });

    $('.suggestion-comment').click(function(){
        let parent = $(this).parents('.jobin-suggestion');
        let modal = $('#suggestion-comment-modal');
        modal.find('.suggestion').html(parent.find('.suggestion').html().toString().trim());
        $('#comment-form').attr('action', $(this).data('url'));
        modal.modal('toggle');
    });

    $('#comment-form').submit(function ( event ) {
        event.preventDefault();

        send_post($(this).attr('action'), $(this));

    });

});




