from rbac.models import DetailInfo, VehicleInfo
from .detail_lib import detail_create,detail_edit
import datetime
from .auth_login import auth


# DataTable获取订单List
def get_cx_tj(request):
    draw = request.POST.get("draw")  # 第几次访问
    dep_id = request.session['dep_id']  # 当前访问部门ID
    roles_id = request.session['roles_id']  # 当前用户角色
    user_id = request.session['user_id']  # 当前用户角色
    cx_no = request.POST.get("cx_no")  # 订单编码
    cx_status = request.POST.get("cx_status")  # 订单状态
    cx_vin = request.POST.get("cx_vin")  # 车辆VIN
    this_page = request.POST.get("this_page")  # 当前页，填报add、审批audit、结算settlement
    start = int(request.POST.get("start"))  # 分页开始
    length = int(request.POST.get("length"))  # 每页条数
    end = start + length

    # 根据角色，初始化查询不同数据
    role_admin = 1  # 系统管理员
    role_fwgw = 3  # 销售顾问
    role_xsjl = 4  # 销售经理
    role_cwsk = 5  # 财务收款

    get_dic = {}  # return
    kwargs = {}
    status_list = []

    if this_page == 'add':
        status_list = [0, 1, 2, 3]
        kwargs["report_name"] = user_id
    if this_page == 'audit':
        if roles_id == role_xsjl:  # 销售经理
            status_list = [1]
            kwargs["department"] = dep_id
    if this_page == 'settlement':
        if roles_id == role_cwsk:  # 财务收款
            status_list = [2]
            kwargs["department"] = dep_id

    if roles_id == role_admin:  # 系统管理员
        status_list = [0, 1]
        kwargs["department"] = dep_id

    if cx_status != "" and int(cx_status) in status_list:
        status_list.clear()
        status_list.append(cx_status)
    kwargs['status__in'] = status_list

    if cx_no != "":
        kwargs['order_no'] = cx_no
    if cx_vin != "":
        kwargs['vin'] = cx_vin

    recordsFiltered = recordsTotal = DetailInfo.objects.filter(**kwargs).count()
    cx_list = list(
        DetailInfo.objects.filter(**kwargs).order_by("-entry_date").values('id', 'order_no', 'order_date',
                                                                           'vehicle__vin',
                                                                           'customer_name',
                                                                           'customer_area', 'status',
                                                                           'vehicle__vehicle_type',
                                                                           'remark',
                                                                           'report_name__last_name', 'settlement_name__last_name', 'auditing_name__last_name',
                                                                           'submit_date', 'auditing_date', 'settlement_date'))[start:end]
    # print(recordsTotal)
    get_dic['draw'] = draw
    get_dic['recordsTotal'] = recordsTotal
    get_dic['recordsFiltered'] = recordsFiltered
    get_dic['data'] = cx_list
    # print(get_dic)
    return get_dic


# 订单详情
@auth
def info_detail(request, nid):
    """
    values_map = map{
        "vehicle",
        "order_no",
        "order_date",
        "customer_name",
        "customer_area",
        "payment_way",
        "payment_nper",
        "transaction_price",
        "security_deposit",
        "replacement_subsidy",
        "gift_je",
        "time_fee",
        "navigation_4G_fee",
        "charging_fee",
        "first_payment",
        "financial_advisory_fee",
        "personal_accident_insurance",
        "mortgage_fee",
        "fs_vps",
        "labor_cost",
        "ln_vps",
        "free_mortgage_fee",
        "installment_bond",
        "glass_insurance",
        "scratch_risk",
        "theft_insurance",
        "extension_insurance",
        "listing_fee",
        "value_added_package",
        "maintenance_package",
        "esc_potential_price",
        "esc_procurement_price",
        "earnest_money",
        "status",
        "department",
        "remark",
        "report_name",
        "auditing_name",
        "settlement_name",
        "entry_date",
        "submit_date",
        "auditing_date",
        "settlement_date"
    }
    :param request:
    :param nid:
    :return:
    """
    values_map = [
        "id",
        "vehicle",
        "order_no",
        "order_date",
        "customer_name",
        "customer_area",
        "payment_way",
        "payment_nper",
        "transaction_price",
        "security_deposit",
        "replacement_subsidy",
        "gift_je",
        "time_fee",
        "navigation_4G_fee",
        "charging_fee",
        "first_payment",
        "financial_advisory_fee",
        "personal_accident_insurance",
        "mortgage_fee",
        "fs_vps",
        "labor_cost",
        "ln_vps",
        "free_mortgage_fee",
        "installment_bond",
        "glass_insurance",
        "scratch_risk",
        "theft_insurance",
        "extension_insurance",
        "listing_fee",
        "value_added_package",
        "maintenance_package",
        "esc_potential_price",
        "esc_procurement_price",
        "earnest_money",
        "status",
        "department",
        "remark",
        "report_name",
        "auditing_name",
        "settlement_name",
        "entry_date",
        "submit_date",
        "auditing_date",
        "settlement_date",
        "lc_ysk_xj",
        "yp_ysk_xj",
        "jr_ysk_xj",
        "bx_ysk_xj",
        "zzb_ysk_xj",
        "ysk_xx",
        "deductions_xj",
        "skzj_xx",
        "dkje_xx"
    ]
    response_data = {}
    try:
        detail_list = list(
            DetailInfo.objects.filter(id=nid).values(*values_map, "vehicle__vin", "vehicle", "vehicle__vehicle_type",
                                                     "vehicle__six_yards", "vehicle__guidance_price",
                                                     "report_name__last_name", "auditing_name__last_name",
                                                     "settlement_name__last_name", "department__title"))

        response_data['detaildata'] = detail_list
        response_data['result'] = 'true'
    except Exception as e:
        response_data['result'] = 'false'
        response_data['message'] = '数据获取失败，请重试！'
        print(e)
    # print(response_data)
    return response_data


# 增加订单
@auth
def add_detail(request):
    dep_id = request.session['dep_id']  # 当前访问部门ID
    vin_id = request.POST.get("vehicle_vin_id")
    response_data = {}  # return

    vehicle_obj = VehicleInfo.objects.filter(id=vin_id).first()  # 订单车辆信息
    # print(vehicle_obj)
    if vehicle_obj:
        if vehicle_obj.status != 0:
            response_data['result'] = 'false'
            response_data['message'] = '此车辆已出售或订单正在审批，请确认！'
        else:
            try:
                # 订单入库
                detail_data = detail_create(request)
                # print(detail_data)
                if int(request.POST.get("sub_val")) == 1:
                    detail_data['status'] = 1
                    DetailInfo.objects.create(**detail_data)
                    # 修改车辆状态
                    VehicleInfo.objects.filter(id=detail_data['vehicle_id']).update(status=2)
                    response_data['result'] = 'true'
                    response_data['message'] = '提交成功！'
                else:
                    detail_data['status'] = 0
                    DetailInfo.objects.create(**detail_data)
                    response_data['result'] = 'true'
                    response_data['message'] = '保存成功！'
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = '提交失败，请联系管理员！'
                print(e)  # todo loging
    else:
        response_data['result'] = 'false'
        response_data['message'] = '无此车辆信息，请确认！'
    return response_data


# 修改订单信息
@auth
def edit_detail(request):
    user_id = request.session['user_id']  # 当前访问部门ID
    user_name = request.session['username']  # 当前访问部门ID
    vin_id = int(request.POST.get("vehicle"))
    order_id = request.POST.get("order_id")
    response_data = {}  # return
    check_data = True

    order_obj = DetailInfo.objects.filter(id=order_id, report_name=user_id).first()  # 订单信息是否为当前操作人
    vehicle_obj = VehicleInfo.objects.filter(id=vin_id).first()  # 订单车辆信息

    if not order_obj:
        check_data = False
        response_data['result'] = 'false'
        response_data['message'] = '无此订单信息，无法进行修改！'

    if not vehicle_obj:
        check_data = False
        response_data['result'] = 'false'
        response_data['message'] = '无此车辆信息，请确认！'

    # print(vehicle_obj)
    if check_data:
        if vehicle_obj.status != 0:
            response_data['result'] = 'false'
            response_data['message'] = '此车辆已出售或订单正在审批，请确认！'
        else:
            try:
                # 订单入库
                detail_data = detail_edit(request)
                # print(detail_data)
                if int(request.POST.get("sub_val")) == 1:
                    detail_data['status'] = 1
                    DetailInfo.objects.filter(id=order_id).update(**detail_data)
                    # 修改车辆状态
                    VehicleInfo.objects.filter(id=vehicle_obj.id).update(status=2)
                    print("--------%s" % vehicle_obj.id)
                    response_data['result'] = 'true'
                    response_data['message'] = '提交成功！'
                    print('<info>:订单编号：%s提交成功，提交人：%s' % (order_obj.order_no, user_name))  # todo loging
                else:
                    detail_data['status'] = 0
                    DetailInfo.objects.filter(id=order_id).update(**detail_data)
                    response_data['result'] = 'true'
                    response_data['message'] = '保存成功！'
                    print('<info>:订单编号：%s保存成功，提交人：%s' % (order_obj.order_no, user_name))  # todo loging
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = '提交失败，请联系管理员！'
                print(e)  # todo loging

    return response_data


# 作废订单
@auth
def del_detail(request):
    response_data = {}
    id = request.POST.get("id")
    user_id = request.session['user_id']
    user_name = request.session['username']
    detail_obj = DetailInfo.objects.filter(id=id, report_name=user_id).values("status", "order_no", "vehicle", "vehicle__vin").first()
    if detail_obj:
        if detail_obj['status'] == 0:  # 订单状态待提交
            try:
                DetailInfo.objects.filter(id=id).update(status=4)
                VehicleInfo.objects.filter(id=detail_obj['vehicle']).update(status=0)
                response_data['result'] = 'true'
                response_data['message'] = "订单已作废！"
                print("<info>-----订单作废，订单号：%s,操作用户：%s.-----" % (detail_obj['order_no'], user_name))
                print("<info>-----车辆状态重置，车辆vin：%s-----" % (detail_obj['vehicle__vin']))
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = "订单作废失败，请联系管理员！"
        else:
            response_data['result'] = 'false'
            response_data['message'] = "只能作废状态为待提交的车辆信息！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "订单数据不存在，请刷新后重试！"
    return response_data


# 撤回订单
@auth
def withdraw_detail(request):
    response_data = {}
    id = request.POST.get("id")
    user_id = request.session['user_id']

    detail_obj = DetailInfo.objects.filter(id=id, report_name=user_id).values("status", "vehicle").first()
    if detail_obj:
        if detail_obj['status'] == 1:  # 订单状态 待审核
            try:
                DetailInfo.objects.filter(id=id).update(status=0)
                VehicleInfo.objects.filter(id=detail_obj['vehicle']).update(status=0)
                response_data['result'] = 'true'
                response_data['message'] = "撤回成功！"
            except Exception as e:
                response_data['result'] = 'false'
                response_data['message'] = "撤回失败，请联系管理员！"
        else:
            response_data['result'] = 'false'
            response_data['message'] = "只能撤回订单状态为待审批的数据！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "数据不存在，请刷新后重试！"
    return response_data


# 审核订单提交
@auth
def audit_detail(request):
    """
    审核订单信息
    :param request:订单id;审核结果：通过、驳回
    :return:
    """
    response_data = {}
    id = request.POST.get("id")  # 订单id
    status_id = int(request.POST.get("status_id"))  # 审批状态 0,驳回，1，通过
    dep_id = request.session['dep_id']
    user_id = request.session['user_id']
    audit_date = datetime.datetime.now()

    detail_obj = DetailInfo.objects.filter(id=id, department=dep_id).values("status").first()
    if detail_obj:
        if detail_obj['status'] == 1:  # 订单状态为 待审批
            if status_id == 1:  # 通过
                try:
                    DetailInfo.objects.filter(id=id).update(status=2, auditing_name=user_id, auditing_date=audit_date)
                    response_data['result'] = 'true'
                    response_data['message'] = "审核完成！"
                except Exception as e:
                    response_data['result'] = 'false'
                    response_data['message'] = "审核失败，请联系管理员！"
            else:  # 驳回
                try:
                    DetailInfo.objects.filter(id=id).update(status=0)
                    response_data['result'] = 'true'
                    response_data['message'] = "订单驳回！"
                except Exception as e:
                    response_data['result'] = 'false'
                    response_data['message'] = "驳回失败，请联系管理员！"
        else:
            response_data['result'] = 'false'
            response_data['message'] = "该订单非待审批状态！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "数据不存在，请刷新后重试！"
    return response_data


# 结算订单提交
@auth
def settlement_detail(request):
    """
    结算订单信息
    :param request:订单id;审核结果：通过、驳回
    :return:
    """
    response_data = {}
    id = request.POST.get("id")  # 订单id
    status_id = int(request.POST.get("status_id"))  # 审批状态 0,驳回，1，通过
    dep_id = request.session['dep_id']
    user_id = request.session['user_id']
    settlement_date = datetime.datetime.now()
    #print('%s,%s,%s'%(id, status_id, dep_id))

    detail_obj = DetailInfo.objects.filter(id=id, department=dep_id).values("status").first()
    if detail_obj:
        if detail_obj['status'] == 2:  # 订单状态为待结算
            if status_id == 1:  # 结算
                try:
                    DetailInfo.objects.filter(id=id).update(status=3, settlement_name=user_id, settlement_date=settlement_date)
                    response_data['result'] = 'true'
                    response_data['message'] = "结算完成！"
                except Exception as e:
                    response_data['result'] = 'false'
                    response_data['message'] = "结算失败，请联系管理员！"
                    print(e)
            else:  # 驳回
                try:
                    DetailInfo.objects.filter(id=id).update(status=1)
                    response_data['result'] = 'true'
                    response_data['message'] = "订单驳回！"
                except Exception as e:
                    response_data['result'] = 'false'
                    response_data['message'] = "驳回失败，请联系管理员！"
                    print(e)
        else:
            response_data['result'] = 'false'
            response_data['message'] = "该订单非待结算状态！"
    else:
        response_data['result'] = 'false'
        response_data['message'] = "数据不存在，请刷新后重试！"
    return response_data