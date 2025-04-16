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
    form.reset();
}

document.getElementById("create_form").addEventListener("submit", handle_create_room)
