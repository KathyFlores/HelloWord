$(document).ready(()=>{
    $('#login-btn').click(()=>{
        $('#login-form').submit(e=>{
            e.preventDefault();
            
        })
        let username = $('#login-username').val();
        let password = $('#login-password').val();
        $.ajax({
            url: login_url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
                username: username,
                password: password
            },
            success: res=>{
                console.log(res);
                if(res.code===200){
                    window.location.reload();
                }
                else{
                    alert(res.msg);
                }
            },
            error: e=>{
                console.log(e);
                
            }
        })
    })
});