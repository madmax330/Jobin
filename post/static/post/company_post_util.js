/**
 * Created by maxencecoulibaly on 5/14/17.
 */



function applicants_navigate(url) {
    let form = $('#filter-form');
    form.attr('action', url);
    form.submit();
}

$(function () {

    /*
     *   SINGLE APPLICANT VIEW FUNCTIONS
     */

    $('.request-cover').click(function () {
        $.get($(this).data('url'), function(data, status){

        if(status === 'success'){
            $('#filter-form').submit();
        }

        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    });

    $('.discard-single-applicant').click(function () {
        let modal = $('#discard-modal');
        modal.find('.name').html($(this).data('name'));
        modal.find('.discard-accepted').attr('data-url', $(this).data('url'));
        modal.modal('show');
    });

    $('.discard-accepted').click(function () {
        $.get($(this).data('url'), function (data, status) {
            if (status === 'success') {
                applicants_navigate($('.single-next').data('url'));
            }
        })
            .fail(function (jqXHR) {
                $('#discard-modal').modal('hide');
                display_message(jqXHR.responseText, 'danger');
            });
    });

    /*
     *   SAVE APPLICATION FUNCTIONS
     */

    $('.save-btn').click(function () {
        $.get($(this).data('url'), function(data, status){

        if(status === 'success'){
            $('#filter-form').submit();
        }

        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    });

    $('.remove-save').click(function () {
        $.get($(this).data('url'), function(data, status){

        if(status === 'success'){
            $('#filter-form').submit();
        }

        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    });


    /*
     *   NAVIGATION
     */

    $('.to-single-view').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.single-next').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.single-prev').click(function () {
        applicants_navigate($(this).data('url'));
    });

    $('.to-multiple-view').click(function () {
        applicants_navigate($(this).data('url'));
    });

});

