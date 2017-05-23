/**
 * Created by maxencecoulibaly on 12/18/16.
 */


$(function(){

    var ids = $('#page-ids').html().split(',');
    var form_id = $('#form-id').html();
    //alert(ids);
    $('.page-number').click(function(){
        for(var i=0; i < ids.length; i++){
            var x = $('#'+ids[i]);
            x.val(x.val() - 1);
            //alert('id: '+ ids[i] + ' val: ' + x.val());
        }
        var num = parseInt($(this).html()) - 1;
        var id = $(this).siblings('.page-object').html();
        //alert('#' + id);
        $('#'+id).val(num);
        //alert(num);
        $('#' + form_id).submit();
    });

});






