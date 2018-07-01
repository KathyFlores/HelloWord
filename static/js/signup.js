$(document).ready(()=>{
    $('#signup-btn').click(()=>{
        $('#signup-form').submit(e=>{
            e.preventDefault();
            
        })
        let username = $('#signup-username').val();
        let email = $('#signup-email').val();
        let password1 = $('#signup-password1').val();
        let password2 = $('#signup-password2').val();
        $.ajax({
            url: signup_url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrftoken,
                username: username,
                email: email,
                password1: password1,
                password2: password2
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