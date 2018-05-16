/**
 * Created by maxencecoulibaly on 7/3/17.
 */



$(function () {

    $('.upload-transcript').click(function () {
        $('#transcriptupload').click();
    });

    $('#transcriptupload').bind('fileuploadsubmit', function (e, data) {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        data.formData = {csrfmiddlewaretoken: csrf};
        if(!(data.formData.csrfmiddlewaretoken)){
            display_message('Error uploading file, reload page and try again.', 'danger');
            return false
        }
    });

    $('#transcriptupload').fileupload({
        dataType: 'json',

        start: function(e) {
            show($('.file-progress'));
        },

        stop: function(e) {
            hide($('.file-progress'));
        },

        done: function (e, data) {
            if(data.result.is_valid) {
                location.reload();
            }
            else {
                display_message(data.result.error, 'danger');
                hide($('.file-progress'));
            }
        }
    });

    $('.delete-transcript').click(function () {
        show($('.file-progress'));
    });

});




