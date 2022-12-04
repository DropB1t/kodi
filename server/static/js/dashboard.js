import getWeather from "./weather.js";
import displayClock from "./time.js"

$(document).ready(function(){
    getWeather()
    displayClock()
    var socket = io.connect(`ws://${document.domain}:${location.port}/dashboard-feed`)
    socket.on('emotion-res', function(msg) {
        
    });
    /* setInterval(() => {
        socket.emit('request-emotion', {})
    }, 5000); */

    setInterval(() => { displayClock() }, 1000);
});
