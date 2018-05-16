/**
 * Created by maxencecoulibaly on 7/3/17.
 */



$(function () {

    $('.upload-logo').click(function () {
        let upload = $('#logo-upload');
        upload.data('url', $(this).data('url'));
        upload.click();
    });

    $('#logo-upload').fileupload({
        dataType: 'json',

        add: function(e, data) {
            data.url = $(this).data('url');
            data.submit();
        },

        start: function(e) {
            show($('.logo-spinner'));
        },

        stop: function(e) {
            hide($('.logo-spinner'));
        },

        done: function (e, data) {
            if(data.result.is_valid) {
                location.reload();
            }
            else {
                display_message(data.result.error, 'danger');
            }
        }
    }).bind('fileuploadsubmit', function (e, data) {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        data.formData = {csrfmiddlewaretoken: csrf};
        if(!(data.formData.csrfmiddlewaretoken)){
            display_message('Error uploading file, reload page and try again.', 'danger');
            return false
        }
    });

    $('.delete-logo').click(function () {
        show($('.logo-spinner'));
    });

});




