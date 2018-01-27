/**
 * Created by maxencecoulibaly on 5/6/17.
 */


function clear_form(id){

    id = '#' + id;
    $(id +' *').filter(':input').each(function(){

        if(!($(this).attr('name') === 'csrfmiddlewaretoken' || $(this).hasClass('skip-form-clear')))
            $(this).val('');
    });

}

function send_post(url, form){

    $.post(url, form.serialize(), function(data, status){

        if(status === 'success'){
            location.reload();
        }

    })
        .fail(function(jqXHR){
            display_message(jqXHR.responseText, 'danger');
        });

}

function send_get(url){

    $.get(url, function(data, status){

        if(status === 'success'){
            location.reload();
        }

    })
        .fail(function(jqXHR){
            display_message(jqXHR.responseText, 'danger');
        });

}

function get_input_date(val){
    if(!isChrome())
        val = val.replace('.', '');
    let temp = new Date(val);
    let day = ("0" + temp.getUTCDate().toString()).slice(-2);
    let month = ("0" + (temp.getMonth() + 1).toString()).slice(-2);
    return temp.getFullYear()+"-"+(month)+"-"+(day)

}

function get_input_time(val){

    let parts = val.split(' ');
    let t = parts[0].split(':');

    let hour = ("0" + val.split(' ')[0].split(':')[0]).slice(-2);
    let min = "00";
    if(t.length === 2)
        min = ("0" + val.split(' ')[0].split(':')[1]).slice(-2);
    if(val.split(' ')[1] === 'p.m.')
        hour = ("0" + (parseInt(hour) + 12)).slice(-2);
    return hour + ':' + min + ':00';

}

function check_cookie(name){
    name = name + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function set_cookie(name, value, t){
    let d = new Date();
    d.setTime(d.getTime() + (t * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/";
}





