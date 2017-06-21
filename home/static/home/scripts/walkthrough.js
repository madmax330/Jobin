/**
 * Created by maxencecoulibaly on 6/9/17.
 */

let CURRENT_WALK = '';

$(function(){

    $(document.body).on('click', '.next-walk', function(){
        let next = $(this).data('next');
        let dir = $(this).data('pos');
        $('.'+CURRENT_WALK).popover('destroy');
        CURRENT_WALK = next;
        $('.'+next).popover({
            content: $('#'+next+'-walkthrough').html(),
            placement: dir,
            container: 'body',
            html: true
        }).popover('show');

    });

    $(document.body).on('click', '.skip-walk', function(){
        $('.'+CURRENT_WALK).popover('destroy');
        CURRENT_WALK = '';
    });

    $('.start-walk').click(function( event ){
        event.preventDefault();
        let first = $('.first-walk');
        let next = first.data('walk');
        CURRENT_WALK = next;
        let dir = first.data('pos');
        $('.'+next).popover({
            content: first.html(),
            placement: dir,
            html: true
        }).popover('show');
    });

    /*

        For students

     */

    let stu = $('.new-student').html();
    if(stu)
        if(stu.toString().trim() === 'true'){
            open_modal('welcome-modal');
        }

    /*

        For companies

     */

    let comp = $('.new-company').html();
    if(comp)
        if(comp.toString().trim() === 'true'){
            $('#welcome-modal').modal('show');
        }

});



