


function new_notification(obj) {

    let code = obj['code'];
    let msg = obj['message'];

    if(code && msg){
        $.notify({
            // options
            icon: code === 'success' ? 'glyphicon glyphicon-check' : 'glyphicon glyphicon-warning-sign',
            title: code === 'success' ? 'Success:' : 'Error:',
            message: msg
        },{
            type: (code === 'success' || code === 'danger') ? code : 'info',
            placement: {
                from: 'top',
                align: 'center'
            },
            mouse_over: 'pause'
        });
    }

}





