/**
 * Created by maxencecoulibaly on 4/27/17.
 */

const MODALS = [
    'warning-modal',
    'resume-modal',
    'language-modal',
    'school-modal',
    'experience-modal',
    'award-modal',
    'skill-modal',
    'welcome-modal'
];

let MODAL_OPEN = false;
let MODAL_BLOCK = false;

$(function(){

    $('body').on('click', function( event ){
         if(MODAL_OPEN && !MODAL_BLOCK){
            for(let i=0; i<MODALS.length; i++){
                let modal = document.getElementById(MODALS[i]);
                if(event.target === modal){
                    close_modal(MODALS[i]);
                    break;
                }
            }
         }
    });

    $('.open-modal').click(function(){
        if(!MODAL_BLOCK)
            open_modal($(this).data('id'));
    });

    $('.close-modal').click(function(){
        if(!MODAL_BLOCK)
            close_modal($(this).data('id'));
    });

    $('.close-notification').click(function(){
        send_get($(this).data('url'));
    });

    $("option[value='All Programs']").remove();

});


function open_modal(id){
    MODAL_OPEN = true;
    document.getElementById(id).style.display = 'block';
    if(WALKTHROUGH !== undefined){
        if(!WALKTHROUGH){
            clear_modal_messages();
        }
    }
    else{
        clear_modal_messages();
    }
}

function close_modal(id){
    MODAL_OPEN = false;
    document.getElementById(id).style.display = 'none';
}

function display_message(msg, code){
    let msgs = $('#messages');

    let html = `<div class="w3-container w3-padding message-${code} w3-display-container">
                    <span onclick="this.parentElement.style.display='none'"
                        class="w3-button w3-display-topright">&times;</span>
                    <p>${msg}</p>
                </div>`;

    msgs.append(html);
    $('html, body').animate({
        scrollTop: $('body').offset().top
    }, 'fast');
}

function display_modal_message(msg, code){
    let msgs = $('.modal-messages');

    let html = `<div class="w3-container w3-padding message-${code} w3-display-container">
                    <span onclick="clear_modal_messages()"
                        class="w3-button w3-display-topright">&times;</span>
                    <p>${msg}</p>
                </div>`;

    msgs.append(html);
}

function hide(obj){
    if(!obj.hasClass('w3-hide'))
        obj.addClass('w3-hide');
}

function show(obj){
    if(obj.hasClass('w3-hide'))
        obj.removeClass('w3-hide');
}

function clear_modal_messages(){
    $('.modal-messages').html('');
}

