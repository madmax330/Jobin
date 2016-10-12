/**
 * Created by maxencecoulibaly on 10/5/16.
 */

$(function(){

    $(".present").each(function(){
        var html = $(this).parent().html();
        html = html + '<button id="curr" class="presentbtn w3-btn w3-light-grey" type="button">Is Current</button>';
        $(this).parent().html(html);
    });

    $("form").on("click", "#curr", function(){
        $("#curr-in").val("True");
        if($(this).hasClass("done")){
            $(".hidden-date").hide();
            $(".current").show();
        }
        else{
            $(this).addClass("done");
            var title = $(".form-script-title").html();
            var html = '<div class="current w3-col s12"><span class="w3-text-green">Is current ' + title + '</span>' +
                '<button id="to-date" class="w3-btn w3-light-grey" style="margin-left:10px;" type="button">Back to date</button></div>';
            var parent = $(this).parent();
            parent.addClass("hidden-date");
            parent.hide();
            var el = $(this).parents(".w3-row").first();
            var base_html = el.html();
            base_html += html;
            el.html(base_html);
        }
    });


    $("form").on("click", "#to-date", function(){
        $("#curr-in").val("False");
        $(".current").hide();
        $(".hidden-date").show();
    });

});


