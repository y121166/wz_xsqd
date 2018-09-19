from rbac.models import DetailMaxNo, Department
import datetime


# 生成最大订单NO
def get_max_no(dep_id):
    """
    生成订单编号，格式：部门编码+月份+流水号，例如：ZD2018090001
    :param dep_id:
    :return: detail_no
    """
    detail_no = ''
    dep_obj = Department.objects.filter(id=dep_id).first()

    dt = datetime.datetime.now().strftime('%Y%m')
    max_no_obj = DetailMaxNo.objects.filter(department=dep_id, date=dt).last()
    if max_no_obj:
        max_no = max_no_obj.max_no + 1
        max_no_str = str(max_no).zfill(3)
        detail_no = '%s%s%s' % (dep_obj.dep_code, dt, max_no_str)
    else:
        max_no = 1
        max_no_str = str(max_no).zfill(3)
        detail_no = '%s%s%s' % (dep_obj.dep_code, dt, max_no_str)

    DetailMaxNo.objects.create(department_id=dep_id, date=dt, max_no=max_no)
    return detail_no


# 订单新增数据项
def detail_create(request):
    """
    订单入库
    :param request:
    :return:data:
    """
    data = {}
    # 前台传入字段
    data["status"] = int(request.POST.get("sub_val"))  # 是否提交
    data["vehicle_id"] = request.POST.get("vehicle_vin_id")  # 车辆vin 0
    data["order_date"] = request.POST.get("order_date")  # 订单日期0
    data["customer_name"] = request.POST.get("customer_name")  # 客户名称0
    data["customer_area"] = request.POST.get("customer_area")  # 客户区域0
    data["payment_way"] = int(request.POST.get("payment_way"))  # 付款方式0
    data["payment_nper"] = int(request.POST.get("payment_nper"))  # 期数2
    # 裸车
    data["transaction_price"] = float(request.POST.get("transaction_price"))  # 成交价0
    data["security_deposit"] = float(request.POST.get("security_deposit"))  # 保险押金0
    data["replacement_subsidy"] = float(request.POST.get("replacement_subsidy"))  # 置换补贴0
    # 用品
    data["gift_je"] = float(request.POST.get("gift_je"))  # 礼包金额0
    data["time_fee"] = float(request.POST.get("time_fee"))  # 工时费0
    data["navigation_4G_fee"] = float(request.POST.get("navigation_4G_fee"))  # 4G导航0
    data["charging_fee"] = float(request.POST.get("charging_fee"))  # 加装金额0
    # 保险
    data["glass_insurance"] = float(request.POST.get("glass_insurance"))  # 玻璃险0
    data["scratch_risk"] = float(request.POST.get("scratch_risk"))  # 划痕险0
    data["theft_insurance"] = float(request.POST.get("theft_insurance"))  # 盗抢险0
    data["extension_insurance"] = float(request.POST.get("extension_insurance"))  # 延保0
    data["listing_fee"] = float(request.POST.get("listing_fee"))  # 挂牌0
    # 增值包
    data["value_added_package"] = float(request.POST.get("value_added_package"))  # 增值包收款0
    data["maintenance_package"] = float(request.POST.get("maintenance_package"))  # 保养套餐0
    # 减项
    data["esc_potential_price"] = float(request.POST.get("esc_potential_price"))  # 二手车评估价格0
    data["esc_procurement_price"] = float(request.POST.get("esc_procurement_price"))  # 二手车收购价格0
    data["earnest_money"] = float(request.POST.get("earnest_money"))  # 已收定金0
    # 基本信息
    data["department_id"] = request.session['dep_id']  # 所属部门0
    data["report_name_id"] = request.session['user_id']  # 填报人0

    # 后台生成字段
    data["submit_date"] = datetime.datetime.now()  # 提交日期
    data["order_no"] = get_max_no(data["department_id"])  # 生成订单NO

    # 小计
    data["lc_ysk_xj"] = data["transaction_price"]+data["security_deposit"]+data["replacement_subsidy"]
    data["yp_ysk_xj"] = data["gift_je"]+data["time_fee"]+data["navigation_4G_fee"]+data["charging_fee"]
    data["bx_ysk_xj"] = data["glass_insurance"]+data["scratch_risk"]+data["theft_insurance"]+data["extension_insurance"]+data["listing_fee"]
    data["zzb_ysk_xj"] = data["value_added_package"]+data["maintenance_package"]
    data["deductions_xj"] = data["esc_potential_price"]+data["esc_procurement_price"]+data["earnest_money"]

    if data["payment_way"] == 0:
        # 全款
        # 应收款
        data["ysk_xx"] =data["lc_ysk_xj"]+data["yp_ysk_xj"]+data["bx_ysk_xj"]+data["zzb_ysk_xj"]
        data["skzj_xx"] = data["ysk_xx"] - data["deductions_xj"]
        return data
    else:
        # 分期
        # 金融
        data["first_payment"] = float(request.POST.get("first_payment"))  # 首付款2
        data["financial_advisory_fee"] = float(request.POST.get("financial_advisory_fee"))  # 金融咨询费2
        data["personal_accident_insurance"] = float(request.POST.get("personal_accident_insurance"))  # 人身意外险2
        data["mortgage_fee"] = float(request.POST.get("mortgage_fee"))  # 抵押费2
        data["fs_vps"] = float(request.POST.get("fs_vps"))  # 方硕VPS2
        data["labor_cost"] = float(request.POST.get("labor_cost"))  # 档案管理、工本材料费2
        data["ln_vps"] = float(request.POST.get("ln_vps"))  # 鲁诺VPS2
        data["free_mortgage_fee"] = float(request.POST.get("free_mortgage_fee"))  # 免抵押费2
        data["installment_bond"] = float(request.POST.get("installment_bond"))  # 分期保证金2

        # 金融小计
        data["jr_ysk_xj"] = data["first_payment"] + data["financial_advisory_fee"] + data["personal_accident_insurance"] + data["mortgage_fee"] + data["fs_vps"] + data["labor_cost"] + data["ln_vps"] + data["free_mortgage_fee"] + data["installment_bond"]

        # 应收款项
        data["ysk_xx"] = data["security_deposit"]+data["replacement_subsidy"] + data["yp_ysk_xj"] + data["jr_ysk_xj"] +  data["bx_ysk_xj"] + data["zzb_ysk_xj"]
        data["skzj_xx"] = data["ysk_xx"] - data["deductions_xj"]
        data["dkje_xx"] = data["transaction_price"] - data["first_payment"]
        return data


# 订单修改数据项
def detail_edit(request):
    """
    订单入库
    :param request:
    :return:data:
    """
    data = {}
    # 前台传入字段
    data["status"] = int(request.POST.get("sub_val"))  # 是否提交
    data["order_date"] = request.POST.get("order_date")  # 订单日期0
    data["customer_name"] = request.POST.get("customer_name")  # 客户名称0
    data["customer_area"] = request.POST.get("customer_area")  # 客户区域0
    data["payment_way"] = int(request.POST.get("payment_way"))  # 付款方式0
    data["payment_nper"] = int(request.POST.get("payment_nper"))  # 期数2
    # 裸车
    data["transaction_price"] = float(request.POST.get("transaction_price"))  # 成交价0
    data["security_deposit"] = float(request.POST.get("security_deposit"))  # 保险押金0
    data["replacement_subsidy"] = float(request.POST.get("replacement_subsidy"))  # 置换补贴0
    # 用品
    data["gift_je"] = float(request.POST.get("gift_je"))  # 礼包金额0
    data["time_fee"] = float(request.POST.get("time_fee"))  # 工时费0
    data["navigation_4G_fee"] = float(request.POST.get("navigation_4G_fee"))  # 4G导航0
    data["charging_fee"] = float(request.POST.get("charging_fee"))  # 加装金额0
    # 保险
    data["glass_insurance"] = float(request.POST.get("glass_insurance"))  # 玻璃险0
    data["scratch_risk"] = float(request.POST.get("scratch_risk"))  # 划痕险0
    data["theft_insurance"] = float(request.POST.get("theft_insurance"))  # 盗抢险0
    data["extension_insurance"] = float(request.POST.get("extension_insurance"))  # 延保0
    data["listing_fee"] = float(request.POST.get("listing_fee"))  # 挂牌0
    # 增值包
    data["value_added_package"] = float(request.POST.get("value_added_package"))  # 增值包收款0
    data["maintenance_package"] = float(request.POST.get("maintenance_package"))  # 保养套餐0
    # 减项
    data["esc_potential_price"] = float(request.POST.get("esc_potential_price"))  # 二手车评估价格0
    data["esc_procurement_price"] = float(request.POST.get("esc_procurement_price"))  # 二手车收购价格0
    data["earnest_money"] = float(request.POST.get("earnest_money"))  # 已收定金0

    # 后台生成字段
    data["submit_date"] = datetime.datetime.now()  # 提交日期

    # 小计
    data["lc_ysk_xj"] = data["transaction_price"]+data["security_deposit"]+data["replacement_subsidy"]
    data["yp_ysk_xj"] = data["gift_je"]+data["time_fee"]+data["navigation_4G_fee"]+data["charging_fee"]
    data["bx_ysk_xj"] = data["glass_insurance"]+data["scratch_risk"]+data["theft_insurance"]+data["extension_insurance"]+data["listing_fee"]
    data["zzb_ysk_xj"] = data["value_added_package"]+data["maintenance_package"]
    data["deductions_xj"] = data["esc_potential_price"]+data["esc_procurement_price"]+data["earnest_money"]

    if data["payment_way"] == 0:
        # 全款
        # 应收款
        data["ysk_xx"] =data["lc_ysk_xj"]+data["yp_ysk_xj"]+data["bx_ysk_xj"]+data["zzb_ysk_xj"]
        data["skzj_xx"] = data["ysk_xx"] - data["deductions_xj"]
        return data
    else:
        # 分期
        # 金融
        data["first_payment"] = float(request.POST.get("first_payment"))  # 首付款2
        data["financial_advisory_fee"] = float(request.POST.get("financial_advisory_fee"))  # 金融咨询费2
        data["personal_accident_insurance"] = float(request.POST.get("personal_accident_insurance"))  # 人身意外险2
        data["mortgage_fee"] = float(request.POST.get("mortgage_fee"))  # 抵押费2
        data["fs_vps"] = float(request.POST.get("fs_vps"))  # 方硕VPS2
        data["labor_cost"] = float(request.POST.get("labor_cost"))  # 档案管理、工本材料费2
        data["ln_vps"] = float(request.POST.get("ln_vps"))  # 鲁诺VPS2
        data["free_mortgage_fee"] = float(request.POST.get("free_mortgage_fee"))  # 免抵押费2
        data["installment_bond"] = float(request.POST.get("installment_bond"))  # 分期保证金2

        # 金融小计
        data["jr_ysk_xj"] = data["first_payment"] + data["financial_advisory_fee"] + data["personal_accident_insurance"] + data["mortgage_fee"] + data["fs_vps"] + data["labor_cost"] + data["ln_vps"] + data["free_mortgage_fee"] + data["installment_bond"]

        # 应收款项
        data["ysk_xx"] = data["security_deposit"]+data["replacement_subsidy"] + data["yp_ysk_xj"] + data["jr_ysk_xj"] +  data["bx_ysk_xj"] + data["zzb_ysk_xj"]
        data["skzj_xx"] = data["ysk_xx"] - data["deductions_xj"]
        data["dkje_xx"] = data["transaction_price"] - data["first_payment"]
        return data
