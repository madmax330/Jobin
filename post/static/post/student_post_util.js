/**
 * Created by maxencecoulibaly on 5/11/17.
 */

/*
 *
 *   POSTS NAVIGATION SCRIPT
 *
 */

let slideIndex = 1;

document.onkeydown = function(e) {
    switch (e.keyCode) {
        case 37:
            plusDivs(1);
            break;
        case 39:
            plusDivs(-1);
            break;
    }
};

function plusDivs(n) {
    increment_post_count($('.viewed-post').find('.increment-url').html().toString().trim());
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

    $('.change-resume').click(function ( event ) {
        event.preventDefault();
        $.get($(this).data('url'), function(data, status){

            if(status === 'success'){
                window.location.replace($('.viewed-post').find('.post-url').html().toString().trim());
            }

        })
            .fail(function(jqXHR){
                display_message(jqXHR.responseText, 'danger');
            });

        send_get(url, null);
    });

    $('.apply').click(function () {
        if(check_cookie('apply'))
            apply($(this).data('url'), $('.viewed-post'));
        else{
            $('#apply-warning').data('url', $(this).data('url'));
            $('.post-warning-name').html($('.viewed-post').find('.display-post-title').html().toString().trim());
            open_modal('apply-modal');
        }
    });

    $('#apply-warning').click(function () {
        if($('#apply-warning-check').is(':checked'))
            set_cookie('apply', 'no warning', 365);
        apply($(this).data('url'), $('.viewed-post'));
    });

    $('.page-link').click(function ( event ) {
        let loc = $('#location_filter').val();
        let key = $('#keyword_filter').val();
        if(loc || key){
            event.preventDefault();
            let form = $('#post-filter-form');
            form.attr('action', $(this).attr('href'));
            form.submit();
        }
    });

});


function apply(url, post) {

    close_modal('apply-modal');
    $('.post-warning-name').html('');

    $.get(url, function(data, status){

        if(status === 'success'){
            let btn = post.find('.apply');
            btn.prop('disabled', true);
            btn.html('Already applied.');
            display_message('Application successful.', 'success');
            plusDivs(1);
        }

    })
        .fail(function(jqXHR){
            display_message(jqXHR.responseText, 'danger');
        });


}


function increment_post_count(url){

    $.get(url, function(data, status){
        console.log('count incremented');
    });

}


