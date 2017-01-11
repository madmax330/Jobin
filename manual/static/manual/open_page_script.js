/**
 * Created by maxencecoulibaly on 1/11/17.
 */


function openPage(evt, page) {
    var i, x, tablinks;
    x = document.getElementsByClassName("man-section");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active-man-section", "");
    }
    document.getElementById(page).style.display = "block";
    evt.currentTarget.firstElementChild.className += " active-man-section";
}





