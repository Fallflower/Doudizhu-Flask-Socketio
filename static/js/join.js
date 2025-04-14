const handle_join_room = (e)=> {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);
    const formObject = Object.fromEntries(formData.entries())
    const roomData = {
        room_id: formObject.room_id,
        password: formObject.password,
    }
    console.log(roomData);

    socket.emit('join_room', roomData);


    form.reset();
}
