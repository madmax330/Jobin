/**
 * Created by maxencecoulibaly on 12/7/16.
 */

$(function(){

    $('#close-all-notes').click(function(){
        var p = $('#page-name').html().toString().replace(/\s+/g, '');
        var url = '/home/closenote/all/student/' + p + '/';
        if(p == 'posts'){
            var post = $('.viewed-post');
            var k = post.find('.pk').html();
            var t = $('.post-type').html();
            url += k + '/' + t + '/';
            //alert(url);
            window.location.href = url;
        }
        else if(p == 'events'){
            var ek = $('.viewed-event').find('.pk').html();
            url += ek + '/' + 'none/';
            //alert(url);
            window.location.href = url;
        }
        else{
            url += '0/none/';
            //alert(url);
            window.location.href = url;
        }

    });

    $('.close-note').click(function(){
        var p = $('#page-name').html().toString().replace(/\s+/g, '');
        var pk = $('.note-key').html();
        var url = '/home/closenote/student/' + pk + '/' + p + '/';
        if(p == 'posts'){
            var post = $('.viewed-post');
            var k = post.find('.pk').html();
            var t = $('.post-type').html();
            url += k + '/' + t + '/';
            //alert(url);
            window.location.href = url;
        }
        else if(p == 'events'){
            var ek = $('.viewed-event').find('.pk').html();
            url += ek + '/' + 'none/';
            //alert(url);
            window.location.href = url;
        }
        else{
            url += '0/none/';
            //alert(url);
            window.location.href = url;
        }

    });

});

