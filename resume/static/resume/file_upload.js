/**
 * Created by maxencecoulibaly on 7/3/17.
 */



$(function () {

    $('.upload-file-resume').click(function () {
        $('#resumeupload').click();
    });

    $('#resumeupload').bind('fileuploadsubmit', function (e, data) {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        data.formData = {csrfmiddlewaretoken: csrf};
        if(!(data.formData.csrfmiddlewaretoken)){
            display_message('Error uploading file, reload page and try again.', 'danger');
            return false
        }
    });

    $('#resumeupload').fileupload({
        dataType: 'json',

        start: function(e) {
            show($('.file-progress'));
        },

        stop: function(e) {
            hide($('.file-progress'));
        },

        progressall: function (e, data) {
            let progress = parseInt(data.loaded / data.total * 100, 10);
            let strProgress = progress + "%";
            let pb = $(".progress-bar");
            pb.css({"width": strProgress});
            pb.text(strProgress);
        },

        done: function (e, data) {
            if(data.result.is_valid) {
                location.reload();
            }
            else {
                display_message(data.result.error, 'danger');
            }
        }
    });

    $('.delete-file-resume').click(function () {
        show($('.spinner'));
    });

});




