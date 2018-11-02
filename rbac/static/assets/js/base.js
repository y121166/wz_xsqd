//base页面自定义JS

function check_psw(obj){
    var data = {}
    var old_psw = $("#old_psw").val();
    var new_psw = $("#new_psw").val();
    var new_psw_again = $("#new_psw_again").val();
    var modal_id = "#modal-password";
    $("#new_psw,#new_psw_again").next().removeClass("red icon-info-sign green icon-ok-circle");
    if(new_psw != new_psw_again){
        $("#new_psw,#new_psw_again").next().addClass("red icon-info-sign");
        $("#new_psw,#new_psw_again").next().html("两次密码不一致");
    }else {
        $("#new_psw,#new_psw_again").next().addClass("green icon-ok-circle");
        data['old_psw'] = old_psw;
        data['new_psw'] = new_psw;
        //ajax提交
        $.ajax({
            url: "/rbac/edit_psw/",
            type: "POST",
            dataType: 'json',
            data: data,
            async: false,
            beforeSend: function () {
                $(obj).addClass("disabled");
                var index = layer.load(1, {shade: true});
            },
            success: function (data, status) {
                layer.close(layer.index);
                layer.msg(data.message);

                if(data.result == 'true'){
                    window.location.reload();
                }else {
                    $(obj).removeClass("disabled");
                }
            },
            error: function (err, status) {
                layer.close(layer.index);
                setTimeout(function () {
                    layer.msg('提交失败,请重试!');
                },500);
                $(obj).removeClass("disabled");
            },
        });
    }
    //console.log(obj);
}

