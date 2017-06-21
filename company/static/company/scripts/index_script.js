/**
 * Created by maxencecoulibaly on 6/16/17.
 */



$(function(){
    let comp = $('.new-company').html().toString().trim();
    if(comp === 'true'){
        $.get('/company/not/new/', function(data, status){
            if(status === 'success'){
            }
        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });
    }
});


