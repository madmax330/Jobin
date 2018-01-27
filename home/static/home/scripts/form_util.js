/**
 * Created by maxencecoulibaly on 5/15/17.
 */



$(function(){

    $('.date-input').each(function(){
        let date = $(this).data('date');
        if(date) {
            $(this).val(get_input_date(date));
            console.log('date: ' + get_input_date(date) + ' value: ' + $(this).val());
        }
        if(!(isChrome() || isFireFox())){
            $(this).datepicker();
        }
    });

    $('.time-input').each(function(){
        let time = $(this).data('time');
        if(time)
            $(this).val(get_input_time(time));
        if(!isChrome()){
            $(this).siblings('label').append(' (hh:mm AM/PM)');
        }
    });

    $('.date-input').click(function ( event ) {
        if(!(isChrome() || isFireFox())){
            event.preventDefault();
        }
    });

});



