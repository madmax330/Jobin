/**
 * Created by maxencecoulibaly on 10/5/16.
 */

$(function(){
    $(".present").each(function(){
        var html = $(this).parent().html();
        html = html + '<button id="pres" class="presentbtn w3-btn w3-light-grey" type="button">Present</button>';
        $(this).parent().html(html);
    });

    $("#pres").click(function(){
        var date = new Date();
        $(this).siblings('input').val(date.toISOString().split('T')[0]);
    });
});


