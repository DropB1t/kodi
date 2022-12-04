/* Weather Request URL https://api.openweathermap.org/data/2.5/weather?lat=43.7159395&lon=10.4018624&lang=en&appid=005dfa6f655e32f1ceca39115347bab6 */

const KELVIN = 273.15;
const weather = {};

export default function getWeather() {
    /* API setted to fetch real time weather in Pisa */
    let api = `https://api.openweathermap.org/data/2.5/weather?lat=43.7159395&lon=10.4018624&lang=en&appid=005dfa6f655e32f1ceca39115347bab6`
    fetch(api)
    .then(function (response) {
        let data = response.json()
        return data
    })
    .then(function (data) {
        weather.temperature = Math.floor(data.main.temp - KELVIN).toFixed(0)
        weather.description = data.weather[0].description
        weather.iconId = data.weather[0].icon
    })
    .then(function () {
        displayWeather()
    });
}

function displayWeather() {
    const widget = $('#weather-widget')
    widget.append(`<span class="text-highlight mr-1">${weather.temperature}°C</span>`); 
    widget.append(`<img class="mx-2" src="../static/img/weather/${weather.iconId}.png"/>`)
    widget.append(`<p class="font-medium text-sm">${weather.description}</p>`);
}
