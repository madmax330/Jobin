/**
 * Created by maxencecoulibaly on 5/11/17.
 */

/*
 *
 *   POSTS NAVIGATION SCRIPT
 *
 */

let slideIndex = 1;

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    $('.viewed-post').removeClass('viewed-post');
    let i;
    let x = document.getElementsByClassName("mySlides");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex - 1].style.display = "block";
    let cp = $(x[slideIndex - 1]);
    cp.addClass('viewed-post');
}

/*
 *
 *   API FUNCTIONS
 *
 */

$(function () {
    showDivs(slideIndex);
    $('html, body').animate({
        scrollTop: $('.job-nav').offset().top
    }, 'slow');

    $('.change-resume').click(function ( event ) {
        event.preventDefault();
        send_get($(this).data('url'), null);
    });

    $('.apply').click(function () {
        apply($(this).data('url'), $('.viewed-post'));
    });

});


function apply(url, post) {

    $.get(url, function(data, status){

        if(status === 'success'){
            let btn = post.find('.apply');
            btn.prop('disabled', true);
            btn.html('Already applied.');
            display_message('Application successful.', 'pale-green');
            $('html, body').animate({
                scrollTop: $('body').offset().top
            }, 'slow');
            plusDivs(1);
        }

    })
        .fail(function(jqXHR){
            display_message(jqXHR.responseText, 'pale-red');
        });


}


