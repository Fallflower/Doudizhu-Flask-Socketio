
function turn_to_login() {
    console.log("Turn to login page");
    window.location.href = "/login.html"
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

        // if (!response.ok) throw new Error("登陆失败");

        const result = await response.json();
        // console.log(result.code)
        if (result.status) {
            alert(`登陆成功！欢迎 ${result.username}}`);
            window.location.replace("/");
        }
        else {
            alert("用户名或密码错误")
            // window.location.replace("/login.html");
            turn_to_login()
        }
        form.reset();
    } catch (error) {
        console.log("Error: ", error);
        alert("网络连接异常")
    }
}
