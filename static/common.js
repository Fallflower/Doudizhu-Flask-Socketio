const socket = io();
socket.on('connect', function () {
    console.log("Connected to game server");
})

socket.on('room_created', (data) => {
    turn_to(`game/${data.room_id}`)
})

function turn_to(e) {
    console.log(`Turn to /${e} page`);
    window.location.href = `/${e}`
}
