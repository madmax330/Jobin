/**
 * Created by maxencecoulibaly on 11/16/16.
 */

$(function(){
    $(window).resize(function(){
        resize_action();
    });
});

function resize_action(){
    let main = $('.w3-main');
    main.hide();
    let w = $(window).width();
    if (w > 1200){
        let rem = w - 1200;
        let val = rem/2;
        main.css('marginLeft', val+'px');
        main.css('marginRight', val+'px');
    }
    else{
        main.css('marginLeft', '30px');
        main.css('marginRight', '30px');
    }
    main.show();
}