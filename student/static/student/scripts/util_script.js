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
    'skill-modal'
];

let MODAL_OPEN = false;
let MODAL_BLOCK = false;

$(function(){

    $('body').on('click', function( event ){
         if(MODAL_OPEN && !MODAL_BLOCK){
            //console.log('Body on click.');
            for(let i=0; i<MODALS.length; i++){
                //console.log('looking for modal: ' + MODALS[i]);
                let modal = document.getElementById(MODALS[i]);
                if(event.target === modal){
                    //console.log('found modal');
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

});


function open_modal(id){
    MODAL_OPEN = true;
    document.getElementById(id).style.display = 'block';
}

function close_modal(id){
    MODAL_OPEN = false;
    document.getElementById(id).style.display = 'none';
}

function display_message(msg, code){
    let msgs = $('#messages');

    let html = `<div class="w3-container w3-${code} w3-display-container">
                    <span onclick="this.parentElement.style.display='none'"
                        class="w3-button w3-display-topright">&times;</span>
                    <p>${msg}</p>
                </div>`;

    msgs.append(html);
}

function display_modal_message(msg, code){
    let msgs = $('.modal-messages');

    let html = `<div class="w3-container w3-${code} w3-display-container">
                    <span onclick="this.parentElement.style.display='none'"
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


