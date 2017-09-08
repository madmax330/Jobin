

function isChrome() {
    let isChromium = window.chrome,
        winNav = window.navigator,
        vendorName = winNav.vendor,
        isOpera = winNav.userAgent.indexOf("OPR") > -1,
        isIEedge = winNav.userAgent.indexOf("Edge") > -1,
        isIOSChrome = winNav.userAgent.match("CriOS");

    if (isIOSChrome) {
        return true;
    } else if (isChromium !== null && isChromium !== undefined && vendorName === "Google Inc." && isOpera === false && isIEedge === false) {
        return true;
    } else {
        return false;
    }
}

function browser_alert(){
    if(!isChrome()) {
        if (!check_cookie()) {
            alert('You are not using Google Chrome!!\nFor better results we suggest that you use Google Chrome as your browser for better results. \n\nThe Jobin Team.');
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