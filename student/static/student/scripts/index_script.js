/**
 * Created by maxencecoulibaly on 6/16/17.
 */



$(function(){
    let stu = $('.new-student').html().toString().trim();
    if(stu === 'true'){
        $.get('/student/not/new/', function(data, status){
            if(status === 'success'){
                open_modal('welcome-modal');
            }
        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    }
});


