/**
 * Created by maxencecoulibaly on 1/9/17.
 */


$(function(){

    var page = $('.curr-page-section').html();
    if(page)
        to_page(page.toString().trim());

    $('.nav-item').click(function(){
        var p = $('#page-name').html().toString().trim();
        var section = $(this).data('sectitle');
        // alert(p);
        if(p == 'home')
            to_page(section);
        else
            window.location.href = '/home/section/' + section + '/';
    });

});

function to_page(p){
    var select = '.' + p + '-section';
    // alert(select);
    if(!(p == 'home')) {
        $('html, body').animate({
            scrollTop: $(select).offset().top
        }, 'slow');
    }
}



