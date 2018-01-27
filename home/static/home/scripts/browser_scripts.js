

function isChrome() {
    // Chrome 1+
    return !!window.chrome && !!window.chrome.webstore;
}

function isFireFox() {
    return typeof InstallTrigger !== 'undefined';
}

function browser_alert(){
    if(!(isChrome() || isFireFox())) {
        if (!check_cookie()) {
            alert('You are not using Google Chrome or Firefox!!\nFor better results we suggest that you use Google Chrome or Firefox as your browser for better results. \n\nThe Jobin Team.');
            set_cookie();
        }
    }
}

function check_cookie(){
    let name = 'jobin_browser_alert' + "=";
    let ca = document.cookie.split(';');
    for(let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function set_cookie(){
    let d = new Date();
    d.setTime(d.getTime() + (1 * 24 * 60 * 60 * 1000));
    let expires = "expires="+d.toUTCString();
    document.cookie = 'jobin_browser_alert' + "=" + 'alerted' + ";" + expires + ";path=/";
}

function check_browsers(){
    // Opera 8.0+
    var isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;

    // Firefox 1.0+
    var isFirefox = typeof InstallTrigger !== 'undefined';

    // Safari 3.0+ "[object HTMLElementConstructor]"
    var isSafari = /constructor/i.test(window.HTMLElement) || (function (p) { return p.toString() === "[object SafariRemoteNotification]"; })(!window['safari'] || (typeof safari !== 'undefined' && safari.pushNotification));

    // Internet Explorer 6-11
    var isIE = /*@cc_on!@*/false || !!document.documentMode;

    // Edge 20+
    var isEdge = !isIE && !!window.StyleMedia;

    // Chrome 1+
    var isChrome = !!window.chrome && !!window.chrome.webstore;

    // Blink engine detection
    var isBlink = (isChrome || isOpera) && !!window.CSS;
}