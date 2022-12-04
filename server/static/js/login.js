import {numpad,alertErr,retryLogin} from './components.js'

$(document).ready(function(){
    var socket = io.connect(`ws://${document.domain}:${location.port}/login-feed`)
    socket.on('new-frame', function(msg) {
        var src = 'data:image/png;base64,' + msg.base64
        $("#camera-frame").attr('src', src)
    });
    socket.on('login-res', function(msg) {
        if (msg.id == -1)
            pinOption()
        else
            dashAccess()
    });
    setInterval(() => {
        socket.emit('request-frame', {})
    }, 100);
});

function pinOption() {
    let cam = $("#cam-div")
    let titleBox = $("#login-action").parent()
    let title = $("#login-action")
    cam.addClass("animate__animated animate__fadeOutUp animate__fast")
    titleBox.addClass("animate__animated animate__fadeOut")
    cam.on('animationend', () => {
        cam.hide()
        $("body").append(numpad)
        $("body").append(alertErr)
        $("body").append(retryLogin)
    });
    titleBox.on('animationend', () => {
        title.html('Insert Pin  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="9" x2="20" y2="9"></line><line x1="4" y1="15" x2="20" y2="15"></line><line x1="10" y1="3" x2="8" y2="21"></line><line x1="16" y1="3" x2="14" y2="21"></line></svg>')
        titleBox.removeClass("animate__fadeOut")
        titleBox.addClass("animate__fadeIn")
    });
}

function dashAccess() {
    location.replace("http://127.0.0.1:5000/dashboard")
}