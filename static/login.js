function turn_to(e) {
    console.log(`Turn to ${e} page`);
    window.location.href = `/${e}`
}

const post_login_info = async (e)=> {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    console.log(formData)

    try {
        const response = await fetch("/api/deal_login", {
            method: "post",
            body: formData
        });

        const result = await response.json();
        // console.log(result.code)
        if (result.status) {
            alert(`登陆成功！欢迎 ${result.User.name}`);
            turn_to("")
        }
        else {
            alert("用户名或密码错误");
            turn_to("login");
        }
        form.reset();
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}
