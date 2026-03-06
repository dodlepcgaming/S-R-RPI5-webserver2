// Ensure Socket.io is initialized
const socket = io();

socket.on('connect', () => {
    console.log("Connected to Pi 5 Webserver");
});

// Listen for the 'update_sensor' event from Python
socket.on('update_sensor', function(data) {
    const display = document.getElementById('distance-val');
    const warning = document.getElementById('warning-msg');

    if (display) {
        display.innerText = data.distance + " mm";
        
        // Logic for your Rover's safety
        if (data.distance < 150) {
            display.style.color = "red";
            warning.innerText = "COLLISION IMMINENT!";
        } else {
            display.style.color = "green";
            warning.innerText = "Path Clear";
        }
    }
});