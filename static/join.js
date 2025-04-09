const handle_join_room = async (e)=> {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    console.log(formData)
    try {
        const response = await fetch("/api/deal_join_room", {
            method: "post",
            body: formData
        });

        const result = await response.json();
        // console.log(result.code)
        if (result.status) {
            turn_to(`game/${result.room_id}`)
        }
        else {
            alert("加入失败。");
        }
        form.reset();
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}
