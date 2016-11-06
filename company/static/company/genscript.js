/**
 * Created by maxencecoulibaly on 11/4/16.
 */
$(function(){

    $('.warning-open').click(function(){
       $(this).siblings('.warning').show();
    });

    $('.warning-close').click(function(){
        $(this).parent().hide();
    });
});





