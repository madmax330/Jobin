/**
 * Created by maxencecoulibaly on 5/11/17.
 */

/*
 *
 *   EVENTS NAVIGATION SCRIPT
 *
 */

let slideIndex = 1;

function plusDivs(n) {
    showDivs(slideIndex += n);
}

function showDivs(n) {
    $('.viewed-event').removeClass('viewed-event');
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
    let ce = $(x[slideIndex - 1]);
    ce.addClass('viewed-event');
}

/*
 *
 *   API FUNCTIONS
 *
 */

$(function () {
    showDivs(slideIndex);
    $('html, body').animate({
        scrollTop: $('.events-header').offset().top
    }, 'slow');

    $('.save').click(function () {
        save($(this).data('url'), $('.viewed-event'));
    });

});


function save(url, event) {

    $.get(url, function (data, status) {

        if (status === 'success') {
            let btn = event.find('.save');
            btn.prop('disabled', true);
            btn.html('Already saved.');
            display_message('Event saved successfully.', 'pale-green');
            $('html, body').animate({
                scrollTop: $('body').offset().top
            }, 'slow');
            plusDivs(1);
        }

    })
        .fail(function (jqXHR) {
            display_message(jqXHR.responseText, 'pale-red');
        });

}






