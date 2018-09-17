
        //获取订单详情
        function detail_info_data(obj){
            $.get("/wzjt/"+$(obj).attr("data_id"),function (data){
                var detail_info_data = eval(data.detaildata)[0];
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
                    //收款总计大写
                    if(span_name == "skzj_dx"){
                        span_val = chineseNumber(detail_info_data.skzj_xx);
                    }
                    //贷款总计
                    if(span_name == "dk_sm"){
                        span_val = detail_info_data.transaction_price - detail_info_data.first_payment;
                    }
                    //订单ID
                    if(span_name =="order_id"){
                        span_val = detail_info_data.id;
                    }
                    $(this).html(span_val);
                });
            });
        }
        //订单审批事件
        function submit_audit_detail(detail_table,data){
            /*
            * data:{
            *  order_id:订单id;
            *  data_id:审批状态;
            * }
            *
            * */
            //alert(id);
            var msg = '';
            if(data.data_id == 1){
                msg = "订单通过？";
            }else{
                msg = "订单驳回？";
            }
            layer.confirm(msg,{icon: 3, title:'提示',btn:['确认','取消']
                    },function () {
                        $.ajax({
                            url:"/wzjt/audit_detail/",
                            type:"POST",
                            dataType:"json",
                            data:{
                                "id":data.order_id,
                                "status_id":data.data_id,
                            },
                            async:false,
                            beforeSend:function(){
                                var index = layer.load(1,{shade:false});
                                $("#modal-audit button[name='audit_detail']").addClass("disabled");
                            },
                            success:function (data,status) {
                                layer.close(layer.index);
                                layer.msg(data.message);
                                if(data.result == 'true'){
                                    setTimeout(function () {
                                        $("#modal-audit").modal('toggle');
                                        detail_table.ajax.reload();
                                     },100);
                                    $("#modal-audit button[name='audit_detail']").removeClass("disabled");
                                }else {
                                    layer.alert(data.message,{
                                        icon:7,
                                        skin: 'layui-layer-lan'
                                        ,closeBtn: 0
                                        ,anim: 4 //动画类型
                                      });
                                    $("#modal-audit button[name='audit_detail']").removeClass("disabled");
                                }
                            },
                            error:function () {
                                layer.close(layer.index);
                                layer.alert("请求失败！",{
                                    icon:7,
                                    skin: 'layui-layer-lan'
                                    ,closeBtn: 0
                                    ,anim: 4 //动画类型
                                  });
                            }
                        });
                    },function () {

                    }
             );
        }
        //页面加载完成后 初始化
        jQuery(function($) {
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

            //审批提交事件
            $("button[name='audit_detail']").on("click",function () {
                var data = {};
                var table_id = "#modal-audit #view_table";
                data.order_id = $(table_id+" span[name='order_id']").text();
                data.data_id = $(this).attr("data_id");
                submit_audit_detail(detail_table,data);
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
                        param.this_page="audit";
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
                    { "data": "report_name__last_name" },
                    { "data": "submit_date" },
                    { "data": "remark" },
                    { "data": "" }
                ],
                //对table格式的定义（表格的列从0开始）
                "columnDefs":[
                    //转义订单状态
                    {
                        targets:7,
                        render:function (data,type,row) {
                            var status_value;
                            switch (row.status){
                                case(1):
                                    status_value = "<span class = 'label label-info arrowed-in-right arrowed'>待审核</span>";
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
                        className: "center",
                        targets:0,
                        data: null,
                        defaultContent:'<input type ="checkbox" name="test" class="icheckbox_minimal" value="">',
                    },
                    {
                        targets:-1, //这一列是id，但是不想再前端显示，"visible": false,表示隐藏
                        render: function(data, type, row, meta) {
                            var caoz_html = '';
                            switch (row.status){
                                case(1):
                                    caoz_html = '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                        '<a class="blue" href="#modal-view" data-toggle="modal" title="详情" data_id="info_detail-'+row.id+ '" name="detail_audit" >\n' +
                                        '<i class="icon-zoom-in bigger-130"></i>\n' +
                                        '</a>'+
                                        '<a class="blue" href="#modal-audit" data-toggle="modal" title="审核"  data_id="info_detail-'+row.id+'" name="detail_audit" >' +
                                        '<i class="icon-flag bigger-130"></i>' +
                                        '</a>' +
                                        '</div>';
                                    break;
                                default:
                                    caoz_html = '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                        '<a class="blue" href="#modal-view" data-toggle="modal" data_id="info_detail-'+row.id+'" title="详情" name="detail_audit" >\n' +
                                        '<i class="icon-zoom-in bigger-130"></i>\n' +
                                        '</a>'+
                                        '</div>';
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

            //table 批量审核按钮
            $("div.toolbar").html('<button class="btn btn-xs btn-primary" onclick="">批量审核</button>');

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

            //审核按钮事件
            $('#detail_table tbody').on('click',"a[name='detail_audit']",function () {
                detail_info_data(this);
                //console.log(this)
            });

            //实现JS添加modal todo
            // $('#detail_table tbody').on("click","a[name='detail_edit']",function () {
            //     //alert(1111);
            //     var id = $(this).attr("data_id");
            //
            //     var initData = {
            //         "appendId": "modal-zw",//加到哪里去
            //         "modalId": "modal-audit",
            //         "title": "订单审批",
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