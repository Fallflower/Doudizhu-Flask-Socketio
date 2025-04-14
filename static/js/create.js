const handle_create_room = (e)=> {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries())
    const roomData = {
        name: formObject.roomname,
        password: formObject.password,
    }
    console.log(roomData);

    socket.emit('create_room', roomData);
    // socket.once('room_created', (response) => {
    //     console.log(response);
    //     if(response.status){
    //         turn_to(`game/${response.room_id}`);
    //     } else {
    //         alert("Failed to create room");
    //     }
    // });
    form.reset();
}
