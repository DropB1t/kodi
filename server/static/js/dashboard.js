import getWeather from "./weather.js";
import displayClock from "./time.js"

const bg = $("#overlay-bg")
const panel = $("#sidepanel")
const emotion = $("#emotion")

const placeList = $("#placeList")
const musicList = $("#musicList")

$(document).ready(function(){
    getWeather()
    displayClock()
    emotion.text("Unknown")
    var socket = io.connect(`ws://${document.domain}:${location.port}/dashboard-feed`)

    socket.on('emotion-res', function(msg) {
        console.log(msg)
        emotion.text(msg)
    });

    socket.on('music-list', function(msg) {
        console.log(msg)
        msg.forEach(element => {
            musicList.append(musicAdv(element.name,element.album))
        });
    });

    socket.on('place-list', function(msg) {
        console.log(msg)
        msg.forEach(element => {
            placeList.append(placeAdv(element.name))
        });
    });

    setInterval(() => {
        socket.emit('request-emotion', {})
    }, 5000);

    $("#overlay-btn").click(function() {
        closePanel()
    });

    $("#info-btn").click(function() {
        openPanel()
    });

    $("#overlay").mouseup(function(e){
        var container = $("#sidepanel");
        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0) 
            closePanel()
    });

    $(document).on('click', 'button#like', function(){
        $(this).children('svg').addClass("fill-tertiary text-tertiary")
        var parent = $(this).parent()
        var parent_id = parent.attr('id')
        if(parent_id == "song"){
            let name = parent.find("#name").text()
            let album = parent.find("#album").text()
            socket.emit('music-up', {name:name, album:album})
        }else if(parent_id == "place"){
            let name = parent.find("#name").text()
            socket.emit('place-up', {name:name})
        }
        parent.removeClass("animate__zoomIn")
        parent.addClass("animate__fadeOut")

        parent.bind('animationend', function(){
            parent.remove()
        });
    });

    setInterval(() => { displayClock() }, 1000);
});

function musicAdv(name,album){
    return `
            <div id="song" class="inline-flex items-center px-2 py-3 bg-background bg-opacity-30 mt-2 rounded-md border-2 border-secondary animate__animated animate__zoomIn animate__faster">
                <svg class="inline mr-3 text-tertiary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle></svg>
                <div class="flex flex-col gap-0">
                    <h3 id="name" class="text-lg font-bold">` + name + `</h3>
                    <p id="album" class="text-xs font-thin">` + album + `</p>
                </div>
                <button id="like" class="ml-auto">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0l-.77.78-.77-.78a5.4 5.4 0 0 0-7.65 0C1.46 6.7 1.33 10.28 4 13l8 8 8-8c2.67-2.72 2.54-6.3.42-8.42z"></path></svg>
                </button>
            </div>
    `
}

function placeAdv(name){
    return `
        <div id="place" class="inline-flex px-2 py-3 bg-background bg-opacity-30 mt-2 rounded-md border-2 border-secondary animate__animated animate__zoomIn animate__faster">
            <svg class="inline mr-3 text-tertiary" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>
            <h3 id="name" class="text-lg font-normal">` + name + `</h3>
            <button id="like" class="ml-auto">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.42 4.58a5.4 5.4 0 0 0-7.65 0l-.77.78-.77-.78a5.4 5.4 0 0 0-7.65 0C1.46 6.7 1.33 10.28 4 13l8 8 8-8c2.67-2.72 2.54-6.3.42-8.42z"></path></svg>
            </button>
        </div>
    `
}

function openPanel(){

    $("#overlay").removeClass("hidden")

    bg.addClass("animate__fadeIn")
    panel.addClass("animate__slideInRight")

    bg.bind('animationend', () => {
        bg.removeClass("animate__fadeIn")
        bg.unbind("animationend")
    });

    panel.bind('animationend', () => {
        panel.removeClass("animate__slideInRight")
        panel.unbind("animationend")
    });
}

function closePanel(){
    bg.addClass("animate__fadeOut")
    panel.addClass("animate__slideOutRight")

    bg.bind('animationend', () => {
        bg.removeClass("animate__fadeOut")
        bg.unbind("animationend")
    });

    panel.bind('animationend', () => {
        panel.removeClass("animate__slideOutRight")
        $("#overlay").addClass("hidden")
        panel.unbind("animationend")
    });
    
}
