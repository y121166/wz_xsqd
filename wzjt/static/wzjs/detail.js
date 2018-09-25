        //生成单选下拉列表 str:JSON格式,selectid : 添加的id
        function createSelect(str,selectid){
            $(selectid).innerHTML='';
            $.each(str,function (i,item) {
                    $(selectid).append("<option value='"+item.id+"'>"+item.title+"</option>");
            });
        }
        //修改触发计算
        function detail_subtotal(obj) {
            var sum = 0;
            var table_id = '#' + $(obj).parents('table').attr("id");
            var tr_id = '#' + $(obj).parents('tr').attr("id");

            $(table_id + " " + tr_id + " .onlyNum").each(function () {
                var num = 0;
                if($(this).val() != ''){
                    num = parseFloat($(this).val());
                }
                sum = sum + num;
                //console.log(sum)
            });
            $(table_id + " " + tr_id + " td:last span").html(sum.toFixed(2));
            detail_ysk_sum(table_id);//应收款项合计
            detail_skzj_diff(table_id);//收款总计

            //贷款合计
            if ($(obj).attr("name") == 'payment_way' || $(obj).attr("name") == 'transaction_price' || $(obj).attr("name") == 'first_payment') {

                if($(table_id + " select[name='payment_way']").val() != 0) {
                    dkzj_sum(table_id);//贷款项合计
                }else {
                $(table_id+" span[name='dkje_xx']").html(0);
                }
            }

            //置换补贴
            if($(obj).attr("name") == 'transaction_price' || $(obj).attr("name") == 'replacement_subsidy' ){
                detail_zhihbt(table_id);
            }
        }
        
        //应收款项
        function detail_ysk_sum(table_id) {
            var sum = 0;
            var num = 0;

            if($(table_id + " select[name='payment_way']").val() == 1){ //分期
                $(table_id + " .fenq").each(function () {
                    num = parseFloat($(this).val());
                    sum = sum + num;
                 });
            }else { //非分期
                $(table_id + " .quank").each(function () {
                    num = parseFloat($(this).val());
                    sum = sum + num;
                });
            }
            $(table_id+" span[name='ysk_xx']").html(sum.toFixed(2));
            $(table_id+" span[name='ysk_dx']").html(chineseNumber(sum));
        }
        
        //贷款总计
        function dkzj_sum(table_id) {
                var dkzj_sum = 0;
                var transaction_price = parseFloat($(table_id + " input[name='transaction_price']").val());
                var first_payment = parseFloat($(table_id + " input[name='first_payment']").val());
                if(transaction_price != 0 && first_payment != 0){
                    dkzj_sum = transaction_price - first_payment;
                }
                $(table_id+" span[name='dkje_xx']").html(dkzj_sum.toFixed(2));
        }

        //收款总计
        function detail_skzj_diff(table_id) {
            var diff = 0;
            var ysk = parseFloat($(table_id+" span[name='ysk_xx']").text());
            var jxk = parseFloat($(table_id+" span[name='deductions_xj']").text());

            diff = ysk - jxk;
            $(table_id+" span[name='skzj_xx']").html(diff.toFixed(2));
            $(table_id+" span[name='skzj_dx']").html(chineseNumber(diff));
        }

         //置换补贴
        function detail_zhihbt(table_id){
            var guidance_price = parseFloat($(table_id + " span[name='vehicle__guidance_price']").text());
            var transaction_price = parseFloat($(table_id + " input[name='transaction_price']").val());
            var replacement_subsidy = parseFloat($(table_id + " input[name='replacement_subsidy']").val());
            //console.log(guidance_price+","+transaction_price+","+replacement_subsidy);
            $(table_id+" span[name='detailZyh']").html((guidance_price - transaction_price - replacement_subsidy).toFixed(2));
        }

        //获取浏览订单详情
        function detail_info_data(obj){
            $.get("/wzjt/"+$(obj).attr("data_id"),function (data){
                var detail_info_data = eval(data.detaildata)[0];
                var detail_head = detail_info_data["department__title"] + " 销售报价单";
                $("#detail_head").children("h3").text(detail_head);
                var table_id = "#view_table";
                $(table_id+" .detail_joinus").each(function () {
                    var span_val = '';
                    var span_name = $(this).attr("name");
                    span_val = detail_info_data[span_name];
                    //分期转义
                    if(span_name == "payment_way"){
                        switch (detail_info_data[span_name]){
                            case 0:
                                span_val = '全款';
                                break;
                            case 1:
                                span_val = '分期';
                                break;
                            case 2:
                                span_val = '返贷';
                                break;
                            case 3:
                                span_val = '理财贷';
                                break;
                            default:
                                span_val = '无';
                        }
                    }
                    //车架号
                    if(span_name == "vehicle_frame_card"){
                        span_val = get_vehicle_card(detail_info_data.vehicle__vin);
                    }
                    //总优惠
                    if(span_name == "detailZyh"){
                        span_val = (detail_info_data.vehicle__guidance_price - detail_info_data.transaction_price - detail_info_data.replacement_subsidy).toFixed(2);
                    }
                    //应收款大写
                    if(span_name == "ysk_dx"){
                        span_val = chineseNumber(detail_info_data.ysk_xx);
                    }
                    if(span_name == 'auditing_date'||span_name =='submit_date'|| span_name == 'settlement_date'){
                        span_val = detail_info_data[span_name];
                        if(span_val != '' && span_val != null){
                            span_val = moment(span_val).format('YYYY-MM-DD HH:mm:ss');
                        }
                    }
                    //收款总计大写
                    if(span_name == "skzj_dx"){
                        span_val = chineseNumber(detail_info_data.skzj_xx);
                    }
                    //贷款总计
                    // if(span_name == "dkje_xx"){
                    //     if(detail_info_data.payment_way != 0){
                    //         span_val = detail_info_data.transaction_price - detail_info_data.first_payment;
                    //     }
                    // }
                    //订单ID
                    if(span_name =="order_id"){
                        span_val = detail_info_data.id;
                    }
                    $(this).html(span_val);
                });
            });
        }

        //获取修改订单详情
        function detail_edit_data(obj){
            $.get("/wzjt/"+$(obj).attr("data_id"),function (data){
                var detail_info_data = eval(data.detaildata)[0];
                var table_id = "#edit_table";
                $(table_id+" .detail_joinus").each(function () {
                    var span_val = '';
                    var span_name = $(this).attr("name");
                    span_val = detail_info_data[span_name];
                    //车架号
                    if(span_name == "vehicle_frame_card"){
                        span_val = get_vehicle_card(detail_info_data.vehicle__vin);
                    }
                    //总优惠
                    if(span_name == "detailZyh"){
                        span_val = (detail_info_data.vehicle__guidance_price - detail_info_data.transaction_price - detail_info_data.replacement_subsidy).toFixed(2);
                    }
                    //应收款大写
                    if(span_name == "ysk_dx"){
                        span_val = chineseNumber(detail_info_data.ysk_xx);
                    }
                    //获取审批日期，结算日期
                    if(span_name == 'auditing_date'||span_name =='submit_date'|| span_name == 'settlement_date'){
                        span_val = detail_info_data[span_name];
                        if(span_val != '' && span_val != null){
                            span_val = moment(span_val).format('YYYY-MM-DD HH:mm:ss');
                        }
                    }
                    //收款总计大写
                    if(span_name == "skzj_dx"){
                        span_val = chineseNumber(detail_info_data.skzj_xx);
                    }
                    //贷款总计
                    if(span_name == "dkje_xx"){
                        if(detail_info_data.payment_way == 1){
                            span_val = detail_info_data.transaction_price - detail_info_data.first_payment;
                        }
                    }
                    //订单ID
                    if(span_name =="order_id"){
                        span_val = detail_info_data.id;
                    }

                    if($(this).prop("tagName") == 'INPUT'){
                        $(this).val(span_val);
                    }

                    if($(this).prop("tagName") == 'SELECT'){
                        //console.log(span_val);
                        $(this).val(span_val);
                        if(detail_info_data['payment_way'] == 1){
                            hiddenShowTr(this);
                        }
                    }
                    if($(this).prop("tagName") == 'SPAN'){
                        $(this).html(span_val);
                    }
                });
            });
        }

        //订单新增保存事件
        function submit_add_detail(detail_table,sub_val){
            var data = {};
            var flag = detail_required("add_table");
            if(flag){
                data["sub_val"] = sub_val;
                $("#add_table input").each(function () {
                  data[$(this).attr("name")] = $(this).val();
                });
                data["payment_way"] = $("#add_table select[name='payment_way']").val();
                //console.log(data);
                $.ajax({
                url: "/wzjt/add_detail/",
                type: "POST",
                dataType: 'json',
                data: data,
                async: false,
                beforeSend: function () {
                    var index = layer.load(1, {shade: true});
                    $("#save_add_detail, #submit_add_detail").addClass("disabled");
                },
                success: function (data, status) {
                    layer.close(layer.index);
                    layer.msg(data.message);

                    if(data.result == 'true'){
                        setTimeout(function () {
                            hide_show_model(0);
                            detail_table.ajax.reload();
                         },100);
                        $("#save_add_detail, #submit_add_detail").removeClass("disabled");
                    }else {
                        $("#save_add_detail, #submit_add_detail").removeClass("disabled");
                    }
                },
                fail: function (err, status) {
                    layer.close(layer.index);
                    setTimeout(function () {
                        layer.msg('提交失败,请重试!');
                    },500);
                    $("#save_add_detail,#submit_add_detail").removeClass("disabled");
                },
                });
            }
        }

        //订单修改保存事件
        function submit_edit_detail(detail_table,sub_val){
            var data = {};
            var flag = detail_required("edit_table");
            if(flag){
                data["sub_val"] = sub_val;
                $("#edit_table input").each(function () {
                  data[$(this).attr("name")] = $(this).val();
                });
                data["payment_way"] = $("#edit_table select[name='payment_way']").val();
                //console.log(data);
                $.ajax({
                url: "/wzjt/edit_detail/",
                type: "POST",
                dataType: 'json',
                data: data,
                async: false,
                beforeSend: function () {
                    var index = layer.load(1, {shade: true});
                    $("#save_edit_detail, #submit_edit_detail").addClass("disabled");
                },
                success: function (data, status) {
                    layer.close(layer.index);
                    layer.msg(data.message);

                    if(data.result == 'true'){
                        setTimeout(function () {
                            hide_show_model(1);
                            detail_table.ajax.reload();
                         },100);
                        $("#save_edit_detail, #submit_edit_detail").removeClass("disabled");
                    }else {
                        $("#save_edit_detail, #submit_edit_detail").removeClass("disabled");
                    }
                },
                fail: function (err, status) {
                    layer.close(layer.index);
                    setTimeout(function () {
                        layer.msg('提交失败,请重试!');
                    },500);
                    $("#save_edit_detail,#submit_edit_detail").removeClass("disabled");
                },
                });
            }
        }

        //订单作废事件
        function submit_del_detail(detail_table,id){
            //alert(id);
            layer.confirm("确定要作废此条数据吗？",{icon: 3, title:'提示',btn:['确认','取消']
                    },function () {
                        $.ajax({
                            url:"/wzjt/del_detail/",
                            type:"POST",
                            dataType:"json",
                            data:{
                                "id":id,
                            },
                            async:false,
                            beforeSend:function(){
                            var index = layer.load(1,{shade:false});
                            },
                            success:function (data,status) {
                                layer.close(layer.index);
                                if(data.result == 'true'){
                                    layer.msg(data.message);
                                    detail_table.ajax.reload();
                                }else {
                                    layer.alert(data.message,{
                                        icon:7,
                                        skin: 'layui-layer-lan'
                                        ,closeBtn: 0
                                        ,anim: 4 //动画类型
                                      })
                                }
                            },
                        });
                    },function () {

                    }
             );
        }

        //订单撤回事件
        function submit_withdraw_detail(vehicle_table,id){
            //alert(id);
            layer.confirm("确定要撤回此条数据吗？",{icon: 3, title:'提示',btn:['确认','取消']
                    },function () {
                        $.ajax({
                            url:"/wzjt/withdraw_detail/",
                            type:"POST",
                            dataType:"json",
                            data:{
                                "id":id,
                            },
                            async:false,
                            beforeSend:function(){
                            var index = layer.load(1,{shade:false});
                            },
                            success:function (data,status) {
                                layer.close(layer.index);
                                if(data.result == 'true'){
                                    layer.msg(data.message);
                                    vehicle_table.ajax.reload();
                                }else {
                                    layer.alert(data.message,{
                                        icon:7,
                                        skin: 'layui-layer-lan'
                                        ,closeBtn: 0
                                        ,anim: 4 //动画类型
                                      })
                                }
                            },
                        });
                    },function () {

                    }
             );
        }

        //显示隐藏hide_show_model框
        function hide_show_model(modal_id){
            switch (modal_id){
                case 0:
                    modal_id = '#modal-add';
                    break;
                case 1:
                    modal_id = '#modal-edit';
                    break;
                default:
                    modal_id = '#modal-edit';
            }
            $(modal_id).modal('toggle');
        }
        
        //获取车架号
        function get_vehicle_card(vin) {
            return vin.substr(-6,6);
        }

        //全款分期
        function hiddenShowTr(obj){
            var table_id = '#' + $(obj).parents('table').attr("id");
            //console.log($(table_id + " .detail_fkfs").val());
           if($(table_id + " .detail_fkfs").val() != 1){
               $(table_id + " .detail_fkqs").val(0);
               $(table_id + " .detail_fkqs").hide();
               $(table_id + " .detail_jr").hide();

               $(table_id + " #jr_add input").each(function () {
                   $(this).val("0.00");
               })
           }else {
               $(table_id + " .detail_fkqs").show();
               $(table_id + " .detail_jr").show();
           }
        }

        //打印
        function print_detail(){
            $(".modal_view").print({
                deferred: $.Deferred(),
                iframe:false,
                append:null,
                prepend:null,
            });
        }

        //页面加载完成后 初始化
        jQuery(function($) {

            //生成vin 自动填充
            $("input[name='vehicle_vin']").autocomplete({
                source:function (request,response) {
                    var vin = $("input[name='vehicle_vin']").val();
                    $.ajax({
                        url:"/wzjt/get_vehicle_vin/",
                        type:"post",
                        dataType:"json",
                        data:{"vin":vin},
                        success:function (data) {
                            //console.log(data);
                            if (data.result){
                                response($.map(data.data,function (item) {
                                    return{
                                        label:item.vin,
                                        id:item.id,
                                        six_yards:item.six_yards,
                                        vehicle_type:item.vehicle_type,
                                        guidance_price:item.guidance_price,
                                        vehicle_frame_card:get_vehicle_card(item.vin),
                                    }
                                }));
                            }else {
                                alert(data.message);
                            }
                        }
                    });
                },
                minLength:3,
                autoFocus:true,
                select: function(event, ui) {
                    var table_id = '#' + $(this).parents('table').attr("id");
                    $(table_id+" input[name='vehicle_vin']").val(ui.item.vin);
                    $(table_id+" input[name='vehicle_vin_id']").val(ui.item.id);
                    $(table_id+" span[name='vehicle_frame_card']").html(ui.item.vehicle_frame_card);
                    $(table_id+" span[name='vehicle_type']").html(ui.item.vehicle_type);
                    $(table_id+" span[name='six_yards']").html(ui.item.six_yards);
                    $(table_id+" span[name='vehicle__guidance_price']").html(ui.item.guidance_price);
                    detail_zhihbt(table_id);
                },
            });

            //重置查询条件事件
            $("#cx_reset").click(function () {
                $("#cx_no").val("");
                $("#cx_vin").val("");
                $("#cx_status").val("");
            });

            //查询事件
            $("#cx_submit").click(function () {
                detail_table.ajax.reload();
            });

            //add_Modal 保存并提交按钮
            $("#submit_add_detail").click(function (){
                submit_add_detail(detail_table,1);
            });
            //add_Modal 保存按钮
            $("#save_add_detail").click(function (){
                submit_add_detail(detail_table,0);
            });

            //edit_modal 保存并提交按钮
            $("#submit_edit_detail").click(function (){
                submit_edit_detail(detail_table,1);
            });

            //edit_modal 保存按钮
            $("#save_edit_detail").click(function (){
                submit_edit_detail(detail_table,0);
            });

            //DataTable初始化
            var detail_table = $("#detail_table").DataTable( {
                // 是否允许排序
                "ordering": false,
                "searching":false,
                "serverSide": true,
                "processing": true,
                "dom":'<"row"<"toolbar col-sm-6"><"col-sm-6 text-right"l>>'+
                        '<"row"<tr>>'+
                        '<"row"<"col-sm-6"i><"col-sm-6"p>>',
                "ajax":{
                    url:"/wzjt/return_detail_list/",
                    type:"POST",
                    data:function (param) {
                        param.cx_status=$("#cx_status").val();
                        param.cx_no=$("#cx_no").val();
                        param.cx_vin=$("#cx_vin").val();
                        param.this_page = 'add';
                        return param;
                    },
                },
                "columns": [
                    { "data":""},
                    {
                        "data":"",
                        render:function (data,type,row,meta) {
                            return meta.settings._iDisplayStart+meta.row+1;
                        }
                    },
                    { "data": "order_no" },
                    { "data": "customer_name" },
                    { "data": "customer_area" },
                    { "data": "vehicle__vehicle_type" },
                    { "data": "vehicle__vin" },
                    { "data": "status" },
                    { "data": "order_date" },
                    { "data": "remark" },
                    { "data": "" }
                ],
                //对table格式的定义（表格的列从0开始）
                "columnDefs":[
                    //转义订单状态
                    {
                        targets:0,
                        className: "center",
                        data: null,
                        defaultContent:'<input type ="checkbox" name="test" class="icheckbox_minimal" value="">',
                    },
                    {
                        targets:2,
                        render:function (data,type,row) {
                            return '<a href="#modal-view"  data-toggle="modal"  data_id="info_detail-'+row.id+'"  name="detail_view" >'+ row.order_no + '</a>'
                        }
                    },
                    {
                        targets:7,
                        render:function (data,type,row) {
                            var status_value;
                            switch (row.status){
                                case(0):
                                    status_value = "<span class = 'label'>待提交</span>";
                                    break;
                                case(1):
                                    status_value = "<span class = 'label label-info arrowed-in-right arrowed'>审核中...</span>";
                                    break;
                                case(2):
                                    status_value = "<span class = 'label label-info arrowed-in-right arrowed'>结算中...</span>";
                                    break;
                                case(3):
                                    status_value = "<span class = 'label label-success'>已完成</span>";
                                    break;
                                case(4):
                                    status_value = "<span class = 'label label-grey'>已废弃</span>";
                                    break;
                            }
                            return status_value;
                        }
                    },
                    {
                        targets:-1, //这一列是id，但是不想再前端显示，"visible": false,表示隐藏
                        render: function(data, type, row, meta) {
                            //最后一个 同时显示多个列的内容
                            //我对这个问题的理解是 比方我有两个字段需要同时显示在一个td里面，或者一个td里面有两个按钮
                            //这个columns.data就完全可以给null了,相应的columns.render().data这里就也是null
                            //按钮的就是自己在里面拼click事件以及对应的按钮样式了
                            var caoz_html = '';
                            switch (row.status){
                                case 0:
                                    caoz_html = '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                        '<a class="blue" href="#modal-view" data-toggle="modal" title="详情" data_id="info_detail-'+row.id+'" name="detail_view" >\n' +
                                        '<i class="icon-zoom-in bigger-130"></i>\n' +
                                        '</a>'+
                                         '<a class="green" href="#modal-edit" data-toggle="modal" title="编辑" data_id="info_detail-'+row.id+'" name="detail_edit" >' +
                                        '<i class="icon-pencil bigger-130"></i>' +
                                        '</a>' +
                                        '<a class="red" href="javascript:void(0);" title="废弃" data_id="'+row.id+'" name="detail_del" >' +
                                        '<i class="icon-trash bigger-130"></i>' +
                                        '</a>' +
                                        '</div>';
                                    break;
                                case 1:
                                    caoz_html = '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                        '<a class="blue" href="#modal-view" data-toggle="modal" data_id="info_detail-'+row.id+'" title="详情" name="detail_view" >\n' +
                                        '<i class="icon-zoom-in bigger-130"></i>\n' +
                                        '</a>'+
                                        '<a class="red" href="javascript:void(0);" title="撤回" data_id="'+row.id+'" name="detail_withdraw" >' +
                                        '<i class="icon-undo bigger-130"></i>' +
                                        '</a>' +
                                        '</div>';
                                    break;
                                default:
                                    caoz_html = '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                        '<a class="blue" href="#modal-detail" data-toggle="modal" title="详情" name="detail_detail" >\n' +
                                        '<i class="icon-zoom-in bigger-130"></i>\n' +
                                        '</a>'+
                                        '</div>';
                                    break;
                            }
                            return caoz_html;
                        }
                    }],
                "createdRow": function(row, data, index) {
                        $(row).data('id',data.id);
                        $(row).find('.icheckbox_minimal').first().val(data.id);
                    },
                "fnDrawCallback": function(){
                    $("#all_checked").prop("checked",false);
                },
                "language": {
                    "processing": "处理中...",
                    "lengthMenu": "显示 _MENU_ 项结果",
                    "zeroRecords": "没有匹配结果",
                    "info": "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
                    "infoEmpty": "显示第 0 至 0 项结果，共 0 项",
                    "loadingRecords": "载入中...",
                    "infoThousands": ",",
                    "paginate": {
                        "first": "首页",
                        "previous": "上页",
                        "next": "下页",
                        "last": "末页"
                    },
                    "decimal": "-",
                    "thousands": "."
                },
            } );

            $('table th input:checkbox').on('click' , function(){
                var that = this;
                $(this).closest('table').find('tr > td:first-child input:checkbox')
                .each(function(){
                    this.checked = that.checked;
                    $(this).closest('tr').toggleClass('selected');
                });
            });

            //table 添加按钮
            $("div.toolbar").html('<button class="btn btn-xs btn-primary" onclick="hide_show_model(0)">添加</button>');

            //实现全选功能
            $("#all_checked").click(function(){
                $('[name=test]:checkbox').prop('checked',this.checked);//checked为true时为默认显示的状态
            });

            //实现反选功能
            $("#checkrev").click(function(){
                $('[name=test]:checkbox').each(function(){
                    this.checked=!this.checked;
                });
            });

            //详情按钮事件
            $('#detail_table tbody').on('click',"a[name='detail_view']",function () {
                detail_info_data(this);
            });

            //编辑按钮事件
            $('#detail_table tbody').on('click',"a[name='detail_edit']",function () {
                detail_edit_data(this);
            });

            //作废事件
            $('#detail_table tbody').on('click',"a[name='detail_del']",function () {
                var id = $(this).attr("data_id");
                submit_del_detail(detail_table,id);
                });

            //撤回
             $('#detail_table tbody').on('click',"a[name='detail_withdraw']",function () {
                var id = $(this).attr("data_id");
                submit_withdraw_detail(detail_table,id);
                });

            //修改金额框触发事件
            $(".onlyNum").on("change",function () {
                if($(this).val() != ''){
                    detail_subtotal(this);
                }else {
                    $(this).val('0.00') ;
                    detail_subtotal(this);
                }
            });

            //根据付款方式隐藏期数,分期
            $(".detail_fkfs").on("click",function () {
                hiddenShowTr(this);
                detail_subtotal(this);
            });

            //class required 必填
            $(".required").on("change",function () {
               hide_icon(this);
            });

            //实现JS添加modal todo
            // $('#detail_table tbody').on("click","a[name='detail_edit']",function () {
            //     //alert(1111);
            //     var id = $(this).attr("data_id");
            //
            //     var initData = {
            //         "appendId": "modal-edit",//加到哪里去
            //         "modalId": "modal-edit",
            //         "title": "修改菜单",
            //         "formId": "formEdit", //form的ID
            //         "loadUrl": "null", //如果不从页面加载，写成"null"
            //         "loadParas": { "ID": id },     //向loadUrl传的数据
            //         "postUrl": "/BasicManage/Edit", //提交add的url
            //         "close": "", //关闭弹出窗后调用的方法
            //         "cols": [{'displayName':'菜单名','fieldName':'Name'}]   //[ {"displayName":"菜单名","fieldName":"Name"}]
            //     };
            //     setModal(initData);
            // });
        });

