# -*- coding: utf-8 -*-
from rbac.models import VehicleInfo
from .auth_login import auth
from rbac.models import Department
import datetime

# 库存导入文件验证
import json


import csv


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


@auth
def del_vehicle(request):
    """
    删除车辆信息
    :param request:
    :return:
    """
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


def get_vehicel_vin(request):
    """
    返回车辆VIN get_vehicel_vin
    :param request:
    :return:
    """
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


def vehicle_import(request):
    """
    批量导入车辆信息
    :param request:
    :return:
    """
    response_data = {}  # result:True,False, msg,all_num ,y_num, n_num, error_list
    file = json.loads(request.POST.get("data"))  # 加载file，json文件
    import_set_list = []  # bulk_create批量提交所需数组
    error_value_list = []  # 重复数据数组
    all_num = y_num = n_num = 0  # 数据量，所有、成功数、失败数

    # 获取所有部门数据
    dep_obj = Department.objects.all()
    all_num = len(file)
    # 遍历JSON
    for key in file:
        if VehicleInfo.objects.filter(vin=key["车辆vin"]).exists():
            n_num = n_num + 1
            error_value_list.append("%s,重复" % key["车辆vin"])
        else:
            y_num = y_num + 1
            VehicleInfo_obj = VehicleInfo(
                vin=key["车辆vin"],
                six_yards=key["六位码"],
                vehicle_type=key["车型"],
                guidance_price=key["指导价"],
                status=0,
                department=Department.objects.get(title=key["所属部门"]),
                inbound_date=datetime.datetime.strptime(key["入库日期"], '%Y/%m/%d').strftime('%Y-%m-%d'),
                remarks=key["备注"],
            )
            import_set_list.append(VehicleInfo_obj)

        try:
            VehicleInfo.objects.bulk_create(import_set_list)
            response_data['result'] = True
        except Exception as e:
            response_data['result'] = False
            error_value_list.clear()
            error_value_list.append("提交数据失败，请联系管理员！")
            print(e)  # todo

    response_data["all_num"] = all_num
    response_data["y_num"] = y_num
    response_data["n_num"] = n_num
    response_data["error_list"] = error_value_list
    return response_data
