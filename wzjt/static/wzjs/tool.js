
/**
* 数字转中文
* @param dValue
* @returns
*/
function chineseNumber(dValue) {
    var maxDec = 2;
    var minus = ""; // 负数的符号"-"的大写："负"字。可自定义字符，如"（负）"。
    var CN_SYMBOL = ""; // 币种名称（如"人民币"，默认空）

    // 验证输入金额数值或数值字符串：
    dValue = dValue.toString().replace(/,/g, "");
    dValue = dValue.replace(/^0+/, ""); // 金额数值转字符、移除逗号、移除前导零
    if (dValue == "") {
        return "零元整";
    } // （错误：金额为空！）
    else if (isNaN(dValue)) {
        return "错误：金额不是合法的数值！";
    }

    if (dValue.length > 1) {
        if (dValue.indexOf('-') == 0) {
                dValue = dValue.replace("-", "");
                minus = "负";
            } // 处理负数符号"-"
            if (dValue.indexOf('+') == 0) {
                dValue = dValue.replace("+", "");
            } // 处理前导正数符号"+"（无实际意义）
    }

    // 变量定义：
    var vInt = "";
    var vDec = ""; // 字符串：金额的整数部分、小数部分
    var resAIW; // 字符串：要输出的结果
    var parts; // 数组（整数部分.小数部分），length=1时则仅为整数。
    var digits, radices, bigRadices, decimals; // 数组：数字（0~9——零~玖）；基（十进制记数系统中每个数字位的基是10——拾,佰,仟）；大基（万,亿,兆,京,垓,杼,穰,沟,涧,正）；辅币（元以下，角/分/厘/毫/丝）。
    var zeroCount; // 零计数
    var i, p, d; // 循环因子；前一位数字；当前位数字。
    var quotient, modulus; // 整数部分计算用：商数、模数。
    // 金额数值转换为字符，分割整数部分和小数部分：整数、小数分开来搞（小数部分有可能四舍五入后对整数部分有进位）。
    var NoneDecLen = (typeof (maxDec) == "undefined" || maxDec == null || Number(maxDec) < 0 || Number(maxDec) > 5); // 是否未指定有效小数位（true/false）
    parts = dValue.split('.'); // 数组赋值：（整数部分.小数部分），Array的length=1则仅为整数。
    if (parts.length > 1) {
        vInt = parts[0];
        vDec = parts[1]; // 变量赋值：金额的整数部分、小数部分
        if (NoneDecLen) {
            maxDec = vDec.length > 5 ? 5 : vDec.length;
        } // 未指定有效小数位参数值时，自动取实际小数位长但不超5。
        var rDec = Number("0." + vDec);
        rDec *= Math.pow(10, maxDec);
        rDec = Math.round(Math.abs(rDec));
        rDec /= Math.pow(10, maxDec); // 小数四舍五入
        var aIntDec = rDec.toString().split('.');
        if (Number(aIntDec[0]) == 1) {
            vInt = (Number(vInt) + 1).toString();
        } // 小数部分四舍五入后有可能向整数部分的个位进位（值1）

        if (aIntDec.length > 1) {
            vDec = aIntDec[1];
        } else {
            vDec = "";
        }
    } else {
        vInt = dValue;
        vDec = "";
        if (NoneDecLen) {
            maxDec = 0;
         }
    }
    if (vInt.length > 44) {
        return "错误：金额值太大了！整数位长【" + vInt.length.toString() + "】超过了上限——44位/千正/10^43（注：1正=1万涧=1亿亿亿亿亿，10^40）！";
    }
    // 准备各字符数组 Prepare the characters corresponding to the digits:
    digits = new Array("零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"); // 零~玖
    radices = new Array("", "拾", "佰", "仟"); // 拾,佰,仟
    bigRadices = new Array("", "万", "亿", "兆", "京", "垓", "杼", "穰", "沟", "涧", "正"); // 万,亿,兆,京,垓,杼,穰,沟,涧,正
    decimals = new Array("角", "分", "厘", "毫", "丝"); // 角/分/厘/毫/丝
    resAIW = ""; // 开始处理

    // 处理整数部分（如果有）
    if (Number(vInt) > 0) {
        zeroCount = 0;
        for (i = 0; i < vInt.length; i++) {
            p = vInt.length - i - 1;
            d = vInt.substr(i, 1);
            quotient = p / 4;
            modulus = p % 4;
            if (d == "0") {
                zeroCount++;
            } else {
                if (zeroCount > 0) {
                    resAIW += digits[0];
                }
                zeroCount = 0;
                resAIW += digits[Number(d)] + radices[modulus];
            }
            if (modulus == 0 && zeroCount < 4) {
                resAIW += bigRadices[quotient];
            }
        }
        resAIW += "元";
    }
    // 处理小数部分（如果有）
    for (i = 0; i < vDec.length; i++) {
        d = vDec.substr(i, 1);
        if (d != "0") {
            resAIW += digits[Number(d)] + decimals[i];
        }
    }
    // 处理结果
    if (resAIW == "") {
        resAIW = "零" + "元";
    } // 零元
    if (vDec == "") {
        resAIW += "整";
    } // …元整
    resAIW = CN_SYMBOL + minus + resAIW; // 人民币/负……元角分/整
    return resAIW;
}


//获取车架号
function get_vehicle_card(vin) {
    return vin.substr(-6,6);
}


//验证必填字段
function detail_required(obj) {
    var xzq = "#"+obj+" .required";
    var results = false;
    $(xzq).each(function () {
        if($(this).val() == ''){
            layer.alert("带"+'<i class="red icon-info-sign bigger-110"></i>'+"为必填项，请检查后再进行提交！",{
                        icon:7,
                        skin: 'layui-layer-lan'
                        ,closeBtn: 0
                        ,anim: 4 //动画类型
                      });
            results = false;
            return true;
        }else {
            results = true;
        }
    });
    return results;
    //console.log(results);
}

//必填icon的显隐性
function hide_icon(obj) {
    if($(obj).val() != ''){
        $(obj).next().css("visibility","hidden");
    }else {
        $(obj).next().css("visibility","visible");
    }
}

//格式化日期
function Format(fmt) {
    var o = {
        "M+" : this.getMonth() + 1,
        "d+" : this.getDate(),
        "h+" : this.getHours(),
        "m+" : this.getMinutes(),
        "s+" : this.getSeconds(),
        "q+" : Math.floor((this.getMonth() + 3) / 3),
        "S" : this.getMilliseconds()
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt))
        fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
};

//读取excel文件

function checkExcel(obj) {
    var req = new Array();
    req['status'] = true;

    //判定是否有文件
    if(obj.files.length==0) {
        req['status'] = false;
        req['msg'] = '必须上传excel文件!';
        layer.msg("必须上传excel文件!");
        return req;
    }

    //获取文件后缀，以判定文件类型
    var suffix = obj.files[0].name.split(".")[1];
    //$('#_file_path').val(obj.files[0].name);
    if(suffix != 'xls' && suffix !='xlsx'){
        req['status'] = false;
        req['msg'] = '只能上传 xls 或 xlsx 格式的文件!';
        layer.msg("只能上传 xls 或 xlsx 格式的文件!");
        return req;
    }

    //判断文件大小
    const IMPORTFILE_MAXSIZE = 10*1024;//这里可以自定义控制导入文件大小
    if(obj.files[0].size/1024 > IMPORTFILE_MAXSIZE){
        req['status'] = false;
        req['msg'] = '文件不能超过10MB!';
        layer.msg("文件不能超过10MB!");
        return req;
    }
    return req;
}

function importExcel(obj, ajax_url) {
    var wb;//读取完成的数据
    var data;//返回的数据

    //ajax
    var timeout = 5*60*1000; //ajax超时时间
    var ajax_url = ajax_url; //url
    var ajax_type = "POST"; //请求方式
    var ajax_async = "false";
    var dataType = 'json';

    var check_flag = checkExcel(obj);
    //console.log(check_result);
    if (!check_flag['status']){
        return;
    }

    var f = obj.files[0]; // 文件内容
    var reader = new FileReader();  // 实例化FileReader对象

    //读取文件为二进制
    reader.readAsBinaryString(f);

    //文件读取完成后的数据处理
    reader.onload = function(e) {
        data = e.target.result;
        //读取为二进制
        wb = XLSX.read(data, {
                type: 'binary'
        });

        var a=wb.SheetNames[0];
        var b=wb.Sheets[a];//内容为方式2

        data = XLSX.utils.sheet_to_json(b);//内容为方式1
        data = JSON.stringify(data);

        if(!data || data==""){
            layer.closeAll('loading');
            layer.msg("文件为空,请选择另一个文件!");
            return;
        }

        console.log(data);
        $.ajax({
            url:ajax_url,
            type:ajax_type,
            dataType:dataType,
            async:ajax_async,
            data:{'data':data},
            beforeSend:function () {
                $("#import_button").addClass("disabled");
            },
            success:function (data,status) {
                $("#file_value").text("");
                $("#error_list").html("");

                var error_list = data.error_list;
                var html = '';

                if(data.result){
                    if(data.n_num == 0){
                        $("#file_value").append('<p>总计：' + data.all_num + '条;   '+ '<span style="color: green">成功：&nbsp' + data.y_num + '&nbsp 条;</span>');
                        layer.alert('导入完成',{
                            skin: 'layui-layer-molv' //样式类名
                            ,closeBtn: 0
                        });
                    }else {
                        $("#file_value").append('<p>总计：' + data.all_num + '条;   '+ '<span style="color: green">成功：&nbsp' + data.y_num + '&nbsp 条;</span>' +
                        '<span style="color: red">失败：&nbsp' + data.n_num + '&nbsp</b>条</span>.<br/>失败明细如下：</p>');

                        for (var i = 0, len = error_list.length; i < len; i++){
                            if(i == 0){
                                html += '<tr><th>序号</th><th>失败VIN及原因</th></tr>'
                            }
                            html += '<tr><td>'+ (i+1) +'</td><td>' + error_list[i] + '</td></tr>'
                        }
                        $("#error_list").append(html);
                        layer.alert('导入完成,失败' + data.n_num + '条',{
                            skin: 'layui-layer-molv' //样式类名
                            ,closeBtn: 0
                        });
                    }


                }else {
                    for (var i = 0, len = error_list.length; i < len; i++){
                        html += '<tr><td>' + error_list[i] + '</td></tr>'
                    }

                    $("#error_list").append(html);

                    layer.alert('导入失败',{
                        skin: 'layui-layer-hong' //样式类名
                        ,closeBtn: 0
                    })
                }
            },
        })

    };


    reader.onloadstart = function (e) {
        var mydate = new Date();
        start = mydate.getTime();
        var loading = layer.load(1, {
          shade: [0.1,'#fff'] //0.1透明度的白色背景
        });
    };

    reader.onprogress = function (e) {
        //读取中 TODO
    };

    reader.onloadend = function (e) {
        var mydate = new Date();
        end = mydate.getTime();
        layer.closeAll(layer.loading);
        console.log((end - start)/1000)
    };
}

//自定义modal内容封装

// function setModal(data) {
//     //初始化
//     var modal = "<div  id='" + data.modalId + "' class='modal fade' tabindex='-1'><div class='modal-dialog'  style='width: 95%'> <div class='modal-content'> <div class='modal-header'> <button type='button' class='close' data-dismiss='modal'><i class='icon-close bigger-110'></i></button><h4 class='modal-title' id='myModalLabel'>" + data.title + "</h4> </div> <div class='modal-body  overflow-visible'> </div> <div class='modal-footer'></div></div></div></div>";
//     $("#" + data.appendId).empty();
//     $("#" + data.appendId).append(modal);
//
//     //加载一个页面的内容
//     if (data.loadUrl != "null") {
//         var form2 = "<form id='" + data.formId + "'>  </form>";
//         $("#" + data.modalId + " .modal-body").append(form2);
//         $("#" + data.formId).load(data.loadUrl, data.loadParas);
//     }
//     else {
//         //获取数据，并填充table
//         var form2 = "<form id='" + data.formId + "' action='" + data.postUrl + "' method='post' >";
//         for (var i = 0; i < data.cols.length; i++) {
//             form2 += " <div > <label  >" + data.cols[i]["displayName"] + "</label> <input type='text' class='form-control' name='" + data.cols[i]["fieldName"] + "' placeholder=''> </div>";
//         }
//         form2 += "</form>";
//         $("#" + data.modalId + " .modal-body").append(form2);
//     }
//     $("#" + data.modalId).modal('show');
//     $("#btn-" + data.modalId).click(function ()
//     {
//         $.post(data.postUrl, $("#" + data.formId).serialize(), function (data) {
//             if (data == "ok") {
//                 alert("添加成功");
//             }
//             else {
//                 alert("添加失败");
//             }
//         });
//
//     });
//
//     $("#btn-close" + data.modalId).click(function () {
//         //data.close();
//     });
// }

