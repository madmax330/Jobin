/**
 * Created by maxencecoulibaly on 7/3/17.
 */



$(function () {

    $('.upload-logo').click(function () {
        $('#logoupload').click();
    });

    $('#logoupload').bind('fileuploadsubmit', function (e, data) {
        let csrf = $('input[name="csrfmiddlewaretoken"]').val();
        data.formData = {csrfmiddlewaretoken: csrf};
        if(!(data.formData.csrfmiddlewaretoken)){
            display_message('Error uploading file, reload page and try again.', 'danger');
            return false
        }
    });

    $('#logoupload').fileupload({
        dataType: 'json',

        start: function(e) {
            show($('.logo-progress'));
        },

        stop: function(e) {
            hide($('.logo-progress'));
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

    $('.delete-logo').click(function () {
        show($('.spinner'));
    });

});




