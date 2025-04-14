const post_register_info = async (e)=> {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    if (formData.get('password') !== formData.get('confirm_password')) {
        alert('两次输入的密码不一致');
        return;
    }

    console.log(formData)

    try {
        const response = await fetch("/api/deal_register", {
            method: "post",
            body: formData
        });

        const result = await response.json();
        // console.log(result.code)
        if (result.status) {
            alert(`注册成功！`);
            turn_to("login.html")
        }
        else {
            alert(result.message)
            turn_to("register.html")
        }
        form.reset();
    } catch (error) {
        console.log("Error: ", error);
        alert("网络连接异常")
    }
}
