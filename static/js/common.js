const socket = io();

socket.on('connect', function () {
    console.log("尝试rejoin")
    socket.emit('rejoin_room', {
        'apply': false
    })
})

socket.on('room_created', (data) => {
    turn_to(`game/${data.room_id}`)
});

socket.on('join_success', (data) => {
    turn_to(`game/${data.room_id}`)
});

socket.on('join_failed', (data) => {
    alert(data.message)
})

function turn_to(e) {
    console.log(`Turn to /${e} page`);
    window.location.href = `/${e}`
}
