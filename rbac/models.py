from django.db import models


class UserInfo(models.Model):
    """用户：划分角色"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    last_name = models.CharField(max_length=32)

    department = models.ForeignKey("Department", null=True, blank=True, on_delete=models.SET_NULL)  # 用户与部门对应关系
    roles = models.ForeignKey('Role', null=True, blank=True, on_delete=models.SET_NULL)  # 用户与角色对应关系

    # 自定义表名
    class Meta:
        db_table = "wz_userinfo"

    def __str__(self):
        return self.last_name


class Department(models.Model):
    title = models.CharField(max_length=64, unique=True)
    dep_code = models.CharField(max_length=5, unique=True, null=True, blank=True)

    class Meta:
        db_table = "wz_department"

    def __str__(self):
        return self.title


class Menu(models.Model):
    # 菜单
    title = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.PROTECT)

    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单

    def __str__(self):
        # 显示层级菜单
        menu_list = [self.title]
        p = self.parent
        while p:
            menu_list.insert(0, p.title)
            p = p.parent
        return '-'.join(menu_list)


class Permission(models.Model):
    """权限"""
    title = models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=128, unique=True)
    is_menu = models.BooleanField(default=False)
    menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}----{permission}'.format(menu=self.menu, permission=self.title)


class Role(models.Model):
    """
    角色：绑定权限
    """
    title = models.CharField(max_length=32, unique=True)

    permissions = models.ManyToManyField("Permission")

    # 定义角色和权限的多对多关系

    def __str__(self):
        return self.title


class VehicleInfo(models.Model):
    """车辆基本信息"""
    vin = models.CharField(max_length=17, unique=True)  # vin
    six_yards = models.CharField(max_length=6)  # 六位码
    vehicle_type = models.CharField(max_length=128)  # 车型
    guidance_price = models.DecimalField(max_digits=10, decimal_places=2)  # 指导价
    status = models.PositiveSmallIntegerField(default=0)  # 车辆状态，0 待售 1 已售 2 审核中
    storage_date = models.DateField(auto_now_add=True)  # 录入日期
    inbound_date = models.DateField()  # 入库日期
    out_date = models.DateField(null=True, blank=True)  # 销售日期
    department = models.ForeignKey("Department", on_delete=models.ProtectedError)  # 所属部门
    remarks = models.CharField(max_length=128, blank=True)  # 备注

    # 自定义表名
    class Meta:
        db_table = "wz_vehicle_info"

    def __str__(self):
        return self.vin


class DetailInfo(models.Model):
    """销售订单信息"""
    vehicle = models.ForeignKey("VehicleInfo", on_delete=models.CASCADE)
    order_no = models.CharField(max_length=20, unique=True)  # 订单唯一编号
    order_date = models.DateField()  # 订单日期
    #vin = models.CharField(max_length=17, unique=True)  # vin
    customer_name = models.CharField(max_length=100)  # 客户姓名
    customer_area = models.CharField(max_length=100)  # 客户区域
    payment_way = models.PositiveSmallIntegerField(default=0)  # 付款方式0:全款 1:分期 2:返贷 3:理财贷
    payment_nper = models.PositiveSmallIntegerField(blank=True, null=True, default=0)  # 具体数值
    transaction_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)  # 成交价
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 保险押金
    replacement_subsidy = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 置换补贴
    lc_ysk_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 裸车小计

    gift_je = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 礼包金额
    time_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 工时费
    navigation_4G_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 4G 导航
    charging_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 加装金额
    yp_ysk_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 用品小计

    first_payment = models.DecimalField(max_digits=9, decimal_places=2, default=0)  # 首付款
    financial_advisory_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 金融咨询费
    personal_accident_insurance = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 人身意外险
    mortgage_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 抵押费
    fs_vps = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 方硕VPS
    labor_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 档案管理、工本材料费
    ln_vps = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 鲁诺VPS
    free_mortgage_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 免抵押费
    installment_bond = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 分期保证金
    jr_ysk_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 金融小计

    glass_insurance = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 玻璃险
    scratch_risk = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 划痕险
    theft_insurance = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 盗抢险
    extension_insurance = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 延保
    listing_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # 挂牌
    bx_ysk_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 保险小计

    value_added_package = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 增值包收款
    maintenance_package = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 保养套餐
    zzb_ysk_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 增值包小计

    ysk_xx = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 应收款

    esc_potential_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 二手车评估价格
    esc_procurement_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 二手车收购价格
    earnest_money = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 已收定金
    deductions_xj = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 扣减小计

    skzj_xx = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 应收款
    dkje_xx = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 贷款金额

    status = models.PositiveSmallIntegerField(default=0)  # 订单状态 0：保存待提交1：待审核2：待结算3：完成4：作废
    department = models.ForeignKey("Department", on_delete=models.ProtectedError)  # 所属部门
    remark = models.CharField(max_length=128, null=True, blank=True)  # 备注
    report_name = models.ForeignKey("UserInfo", related_name="report_UserInfo", on_delete=models.ProtectedError)  # 填报人

    sales_consultant = models.CharField(max_length=100, null=True, blank=True)  # 销售顾问

    auditing_name = models.ForeignKey("UserInfo", related_name="auditing_UserInfo", null=True, blank=True,
                                      on_delete=models.ProtectedError)  # 审核人
    settlement_name = models.ForeignKey("UserInfo", related_name="settlement_UserInfo", null=True, blank=True,
                                        on_delete=models.ProtectedError)  # 结算人
    entry_date = models.DateTimeField(auto_now_add=True)  # 录入日期,不可修改
    submit_date = models.DateTimeField(blank=True, null=True)  # 提交日期
    auditing_date = models.DateTimeField(blank=True, null=True)  # 审核日期
    settlement_date = models.DateTimeField(blank=True, null=True)  # 结算日期

    # 自定义表名
    class Meta:
        db_table = "wz_detail_info"

    def __str__(self):
        return self.order_no


class DetailMaxNo(models.Model):
    department = models.ForeignKey("Department", on_delete=models.CASCADE)  # 用户与部门对应关系
    date = models.CharField(max_length=6)
    max_no = models.PositiveIntegerField()

    # 自定义表名
    class Meta:
        db_table = "wz_detail_maxno"

    def __str__(self):
        return self.max_no
