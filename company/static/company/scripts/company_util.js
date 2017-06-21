/**
 * Created by maxencecoulibaly on 5/14/17.
 */


function hide(obj){
    if(!obj.hasClass('hidden'))
        obj.addClass('hidden');
}

function show(obj){
    if(obj.hasClass('hidden'))
        obj.removeClass('hidden');
}

function display_message(msg, code){
    let msgs = $('.messages');

    let html = `<div class="alert alert-dismissable alert-${code}">
                    <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
                    <p>${msg}</p>
                </div>`;

    msgs.append(html);
    $('html, body').animate({
        scrollTop: $('body').offset().top
    }, 'fast');
}





