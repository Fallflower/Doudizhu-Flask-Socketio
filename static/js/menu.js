const apply_go_back = () => {
    socket.emit('rejoin_room', {
        'apply': true,
    })
}