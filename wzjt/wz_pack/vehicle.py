from rbac.models import VehicleInfo
from .auth_login import auth


# DataTable获取车辆List
def get_cx_tj(request):
    draw = request.POST.get("draw")  # 第几次访问
    dep_id = request.session['dep_id']  # 当前访问部门ID
    cx_vin = request.POST.get("cx_vin")  # vin
    cx_status = request.POST.get("cx_status")  # 车辆状态
    start = int(request.POST.get("start"))  # 分页开始
    length = int(request.POST.get("length"))  # 每页条数
    end = start + length

    get_dic = {}  # return

    kwargs = {  # 多查询条件
        "department": dep_id,
    }
    if cx_vin != "":
        kwargs['vin__icontains'] = cx_vin
    if cx_status != "":
        kwargs['status'] = cx_status

    recordsFiltered = recordsTotal = VehicleInfo.objects.filter(**kwargs).count()
    cx_list = list(
        VehicleInfo.objects.filter(**kwargs).order_by("-storage_date").values('id', 'vin', 'six_yards',
                                                                              'vehicle_type',
                                                                              'guidance_price', 'status',
                                                                              'storage_date',
                                                                              'remarks'))[start:end]
    # print(recordsTotal)
    get_dic['draw'] = draw
    get_dic['recordsTotal'] = recordsTotal
    get_dic['recordsFiltered'] = recordsFiltered
    get_dic['data'] = cx_list
    # print(get_dic)
    return get_dic


# 增加车辆信息
@auth
def add_vehicle(request):
    vin = request.POST.get("vin")
    vehicle_type = request.POST.get("vehicle_type")
    six_yards = request.POST.get("six_yards")
    guidance_price = request.POST.get("guidance_price")
    dep_select = int(request.POST.get("dep_select"))
    remarks = request.POST.get("remarks")
    response_data = {}

    vin_info = VehicleInfo.objects.filter(vin=vin)
    if vin_info:
        response_data['result'] = 'false'
        response_data['message'] = '车辆VIN已存在，请确认。'
    else:
        try:
            VehicleInfo.objects.create(vin=vin, vehicle_type=vehicle_type, six_yards=six_yards, status=0,
                                       guidance_price=guidance_price, department_id=dep_select, remarks=remarks)
            response_data['result'] = 'true'
            response_data['message'] = '提交成功！'
        except Exception as e:
            response_data['result'] = 'false'
            response_data['message'] = '提交失败，请联系管理员！'
    return response_data


# 修改车辆信息
@auth
def edit_vehicle(request):
    dep_id = request.session['dep_id']
    id = request.POST.get("id")
    vehicle_type = request.POST.get("vehicle_type")
    six_yards = request.POST.get("six_yards")
    guidance_price = request.POST.get("guidance_price")
    dep_select = int(request.POST.get("dep_select"))
    remarks = request.POST.get("remarks")
    response_data = {}
    Vehicle_obj = VehicleInfo.objects.filter(id=id, department=dep_id).values("status").first()

    if Vehicle_obj:
        if Vehicle_obj['status'] == 0:
            try:
                VehicleInfo.objects.filter(id=id).update(vehicle_type=vehicle_type, six_yards=six_yards,
                                                         guidance_price=guidance_price, department_id=dep_select,
                                                         remarks=remarks)
                response_data['result'] = 'true'
                response_data['message'] = '提交成功！'
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = '提交失败，请联系管理员！'
        else:
            response_data['result'] = 'false'
            response_data['message'] = "只能删除状态为待售的车辆信息！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "数据不存在，请刷新后重试！"

    return response_data


# 删除车辆信息
@auth
def del_vehicle(request):
    response_data = {}
    id = request.POST.get("id")
    dep_id = request.session['dep_id']

    Vehicle_obj = VehicleInfo.objects.filter(id=id, department=dep_id).values("department_id", "status").first()
    if Vehicle_obj:
        if Vehicle_obj['status'] == 0:
            try:
                VehicleInfo.objects.filter(id=id).delete()
                response_data['result'] = 'true'
                response_data['message'] = "删除成功！"
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = "删除失败，请联系管理员！"
        else:
            response_data['result'] = 'false'
            response_data['message'] = "只能删除状态为待售的车辆信息！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "车辆数据不存在，请刷新后重试！"
    return response_data


# 返回车辆VIN get_vehicel_vin
def get_vehicel_vin(request):
    vin = request.POST.get("vin")
    dep_id = request.session['dep_id']
    response_data = {}
    try:
        cx_list = list(
            VehicleInfo.objects.filter(vin__icontains=vin, department=dep_id, status=0).values('id', 'vin', 'six_yards',
                                                                                               'vehicle_type',
                                                                                               'guidance_price'))[0:10]
        response_data['data'] = cx_list
        response_data['result'] = 'true'
    except Exception as e:
        response_data['result'] = 'false'
        response_data['message'] = '获取车辆vin列表失败，请联系管理员！'
    return response_data
