        //生成单选下拉列表 str:JSON格式,selectid : 添加的id
        function createSelect(str,selectid){
            $(selectid).innerHTML='';
            $.each(str,function (i,item) {
                    $(selectid).append("<option value='"+item.id+"'>"+item.title+"</option>");
            });
        }

        //车辆添加提交事件
        function submit_add_vehicle(vehicle_table){
            var flag = $("#add_vehicle_form").valid();//JS验证表单数据有效性
            if(flag){
                var vin = $("#add_vin").val();
                var vehicle_type = $("#add_vehicle_type").val();
                var six_yards = $("#add_six_yards").val();
                var guidance_price = $("#add_guidance_price").val();
                var dep_select = $("#add_dep_select").val();
                var remarks = $("#add_remarks").val();
                //console.log(username,last_name,dep_select,roles_select)
                $.ajax({
                    url: "/wzjt/add_vehicle/",
                    type: "POST",
                    dataType: 'json',
                    data: {
                        "vin": vin,
                        "vehicle_type": vehicle_type,
                        "six_yards": six_yards,
                        "guidance_price": guidance_price,
                        "dep_select": dep_select,
                        "remarks": remarks,
                    },
                    async: false,
                    beforeSend: function () {
                        var index = layer.load(1, {shade: false});
                    },
                    success: function (data, status) {
                        layer.close(layer.index);
                        layer.msg(data.message);

                        if(data.result == 'true'){
                            setTimeout(function () {
                                add_model();
                                vehicle_table.ajax.reload();
                             },100);
                        }
                    },
                    fail: function (err, status) {
                        layer.close(layer.index);
                        setTimeout(function () {
                            layer.msg('提交失败,请重试!');
                        },500);
                    },
                });
            }
        }

        //车辆修改事件
        function submit_edit_vehicle(vehicle_table){
            var flag = $("#edit_vehicle_form").valid();//JS验证表单数据有效性
            if(flag){
                var id = $("#id").val();
                var vin = $("#vin").val();
                var vehicle_type = $("#vehicle_type").val();
                var six_yards = $("#six_yards").val();
                var guidance_price = $("#guidance_price").val();
                var dep_select = $("#dep_select").val();
                var remarks = $("#remarks").val();
                //console.log(username,last_name,dep_select,roles_select)
                $.ajax({
                    url: "/wzjt/edit_vehicle/",
                    type: "POST",
                    dataType: 'json',
                    data: {
                        "id":id,
                        "vin": vin,
                        "vehicle_type": vehicle_type,
                        "six_yards": six_yards,
                        "guidance_price": guidance_price,
                        "dep_select": dep_select,
                        "remarks": remarks,
                    },
                    async: false,
                    beforeSend: function () {
                        var index = layer.load(1, {shade: false});
                    },
                    success: function (data, status) {
                        layer.close(layer.index);
                        layer.msg(data.message);

                        if(data.result == 'true'){
                            setTimeout(function () {
                                edit_model();
                                vehicle_table.ajax.reload();
                             },100);
                        }
                    },
                    fail: function (err, status) {
                        layer.close(layer.index);
                        setTimeout(function () {
                            layer.msg('提交失败,请重试!');
                        },500);
                    },
                });
            }
        }

        //车辆删除事件
        function submit_del_vehicle(vehicle_table,id){
            //alert(id);
            layer.confirm("确定要删除此条数据吗？",{icon: 3, title:'提示',btn:['确认','取消']
                    },function () {
                        $.ajax({
                            url:"/wzjt/del_vehicle/",
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

        //显示隐藏add_model框
        function add_model(){
            $('#modal-add').modal('toggle');
        }

        //显示隐藏add_model框
        function edit_model(){
            $('#modal-edit').modal('toggle');
        }

        //页面加载完成后 初始化
        jQuery(function($) {
            //初始化add_form表单验证
            $("#add_vehicle_form").validate({
                rules: {
                    add_vin: {
                      required:true,
                      minlength:17,
                      maxlength:17,
                    },
                    add_vehicle_type: "required",
                    add_six_yards: {
                    required: true,
                    minlength:6,
                      maxlength:6,
                    },
                    add_guidance_price: {
                    required: true,
                    number:true,
                    },
                    add_dep_select: "required",
                    },
                    messages: {
                    add_vin: {
                    required: "请输入车辆VIN码",
                    maxLength:"车辆VIN码最多17位",
                    minlength: "车辆VIN码最少17位"
                    },
                    add_vehicle_type: "请输入车型",
                    add_six_yards: {
                    required: "六位码未生成，请输入vin",
                    minlength: "请输入正确的六位码",
                    maxlength:"请输入正确的六位码"
                    },
                    add_guidance_price: {
                      required:"请输入车辆指导价格",
                      number:"请输入数值",
                    },
                    add_dep_select: "请选择所属部门",
                    }
                });

            //初始化edit_form表单验证
            $("#edit_vehicle_form").validate({
                rules: {
                    vin: {
                      required:true,
                      minlength:17,
                      maxlength:17,
                    },
                    vehicle_type: "required",
                    six_yards: {
                        required: true,
                        minlength:6,
                        maxlength:6,
                    },
                    guidance_price: {
                        required: true,
                        number:true,
                    },
                    dep_select: "required",
                    },
                    messages: {
                    vin: {
                        required: "请输入车辆VIN码",
                        maxLength:"车辆VIN码最多17位",
                        minlength: "车辆VIN码最少17位"
                    },
                    vehicle_type: "请输入车型",
                    six_yards: {
                        required: "六位码未生成，请输入vin",
                        minlength: "请输入正确的六位码",
                        maxlength:"请输入正确的六位码"
                    },
                    guidance_price: {
                        required:"请输入车辆指导价格",
                        number:"请输入数值",
                    },
                    dep_select: "请选择所属部门",
                    }
                });

            //重置查询条件事件
            $("#cx_reset").click(function () {
                $("#cx_vin").val("");
                $("#cx_status").val("");
            });

            //查询事件
            $("#cx_submit").click(function () {
                vehicle_table.ajax.reload();
            });

            //add_Modal 保存按钮
            $("#submit_add_vehicle").click(function (){
                submit_add_vehicle(vehicle_table);
            });

            //edit_modal 保存按钮
            $("#submit_edit_vehicle").click(function (){
                submit_edit_vehicle(vehicle_table);
            });

            //根据VIN号，计算车架号
            /*
            $("#add_vin,#vin").on('blur',function () {
                if(this.id == "add_vin"){
                    $("#add_six_yards").val($("#add_vin").val().substr(-6,6));
                }else{
                    $("#six_yards").val($("#vin").val().substr(-6,6));
                }
            });*/

            //初始化select值
            $.get("/rbac/user_init_select/",function (data) {
                var dep_info = eval(data.depinfo);
                createSelect(dep_info, ".dep_select");
            });


            //DataTable初始化
            var vehicle_table = $("#vehicle_table").DataTable( {
                // 是否允许排序
                "ordering": false,
                "searching":false,
                "serverSide": true,
                "processing": true,
                "dom":'<"row"<"toolbar col-sm-6"><"col-sm-6 text-right"l>>'+
                        '<"row"<tr>>'+
                        '<"row"<"col-sm-6"i><"col-sm-6"p>>',
                //"pagingType":"numbers",
                //"order": [7,'asc'],
                "ajax":{
                    url:"/wzjt/return_car_list/",
                    type:"POST",
                    data:function (param) {
                        param.cx_status=$("#cx_status").val();
                        param.cx_vin=$("#cx_vin").val();
                        return param;
                    }
                },
                "columns": [
                    { "data":""},
                    {
                        "data":"",
                        render:function (data,type,row,meta) {
                            return meta.settings._iDisplayStart+meta.row+1;
                        }
                    },
                    { "data": "vin" },
                    { "data": "six_yards" },
                    { "data": "vehicle_type" },
                    { "data": "guidance_price" },
                    { "data": "status" },
                    { "data": "storage_date" },
                    { "data": "remarks" },
                    { "data": "" }
                ],
                //对table格式的定义（表格的列从0开始）
                "columnDefs":[
                    //转义车辆状态
                    {
                        targets:6,
                        render:function (data,type,row) {
                            var status_value;
                            switch (row.status){
                                case(0):
                                    status_value = "待售";
                                    break;
                                case(1):
                                    status_value = "已售";
                                    break;
                                case(2):
                                    status_value = "审核中";
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
                            //最后一个 同时显示多个列的内容
                            //我对这个问题的理解是 比方我有两个字段需要同时显示在一个td里面，或者一个td里面有两个按钮
                            //这个columns.data就完全可以给null了,相应的columns.render().data这里就也是null
                            //按钮的就是自己在里面拼click事件以及对应的按钮样式了
                            if(row.status == 0){
                                return '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                '   <a class="blue" href="#modal-detail" data-toggle="modal" name="vehicle_detail" >\n' +
                                '   <i class="icon-zoom-in bigger-130"></i>\n' +
                                '   </a>\n' +'\n' +
                                '   <a class="green" href="#modal-edit" data-toggle="modal" id = "vehicle_info-' + row.id + '" name="vehicle_info" >\n' +
                                '   <i class="icon-pencil bigger-130"></i>\n' +
                                '   </a>\n' +
                                '\n' + '<a class="red" href="#" id="vehicle_del-'+ row.id +'" data_id="'+row.id+'" name="vehicle_del">\n' +
                                '   <i class="icon-trash bigger-130"></i>\n' +
                                '    </a>\n' +
                                '    </div>'
                            }else {
                                return '<div class="visible-md visible-lg hidden-sm hidden-xs action-buttons">\n' +
                                '   <a class="blue" href="#modal-detail" data-toggle="modal" name="vehicle_detail" >\n' +
                                '   <i class="icon-zoom-in bigger-130"></i>\n' +
                                '   </a>\n' +'\n'
                            }
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
                }
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
            $("div.toolbar").html('<button class="btn btn-xs btn-primary" onclick="add_model()">添加</button>');

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

            //add_modal 关闭自动清除填写信息
            $('#modal-add').on('hidden.bs.modal', function () {
                $("#add_vin").val("");
                $("#add_vehicle_type").val("");
                $("#add_six_yards").val("");
                $("#add_guidance_price").val("0.00");
                $("#add_dep_select").val("");
                $("#add_remarks").val("");
            });

            //获取车辆详情
            $('#vehicle_table tbody').on('click',"a[name='vehicle_info']",function () {
                $.get("/wzjt/"+this.id,function (data){
                    //console.log(data)
                    var vehicle_info = eval(data.vehicledata);
                    $.each(vehicle_info,function (i , item) {
                        $("#id").attr("value",item.id);
                        $("#vin").attr("value",item.vin);
                        $("#vehicle_type").attr("value",item.vehicle_type);
                        $("#six_yards").attr("value",item.six_yards);
                        $("#guidance_price").attr("value",item.guidance_price);
                        $("#dep_select").val(item.department);
                        $("#storage_date").attr("value",item.storage_date);
                        $("#out_date").attr("value",item.out_date);
                        $("#remarks").attr("value",item.remarks);
                    });
                });
            });

            //删除事件
            $('#vehicle_table tbody').on('click',"a[name='vehicle_del']",function () {
                var id = $(this).attr("data_id");
                submit_del_vehicle(vehicle_table,id);
                });
        });