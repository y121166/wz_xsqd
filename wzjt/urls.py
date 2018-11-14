from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index/$', views.index, name='index'),

    # 车辆信息相关
    url(r'^vehicle_list/$', views.car_list, name='car_list'),  # 库存列表
    url(r'^get_vehicle_vin/$', views.get_vehicle_vin, name='get_vehicle_vin'),  # 车辆vin
    url(r'^return_car_list/$', views.return_car_list, name='return_car_list'),  # 库存列表
    url(r'^add_vehicle/$', views.add_vehicle, name='add_vehicle'),  # 增加车辆
    url(r'^edit_vehicle/$', views.edit_vehicle, name='edit_vehicle'),  # 修改车辆信息
    url(r'^del_vehicle/$', views.del_vehicle, name='del_vehicle'),  # 删除车辆信息
    url(r'^vehicle_info-(?P<nid>\d+)/$', views.vehicle_info, name='vehicle_info'),  # 车辆信息详情
    url(r'^vehicle_import/$', views.vehicle_import, name='vehicle_import'),  # 导入车辆信息
    url(r'^vehicle_down/$', views.vehicle_down, name='vehicle_down'),  # 下载导入模板

    # 订单相关
    url(r'^detail_page/$', views.detail_page, name='detail_page'),  # 销售顾问
    url(r'^detail_audit_page/$', views.detail_audit_page, name='detail_audit_page'),  # 销售经理
    url(r'^detail_settlement_page/$', views.detail_settlement_page, name='detail_settlement_page'),  # 财务专员
    url(r'^detail_print-(?P<nid>\d+)/$', views.detail_print, name='detail_print'),  # 打印页面

    url(r'^return_detail_list/$', views.return_detail_list, name='return_detail_list'),  # 返回订单列表
    url(r'^add_detail/$', views.add_detail, name='add_detail'),  # 添加订单
    url(r'^edit_detail/$', views.edit_detail, name='edit_detail'),  # 修改订单
    url(r'^info_detail-(?P<nid>\d+)/$', views.info_detail, name='info_detail'),  # 订单详情
    url(r'^withdraw_detail/$', views.withdraw_detail, name='withdraw_detail'),  # 撤回订单
    url(r'^del_detail/$', views.del_detail, name='del_detail'),  # 废弃订单
    url(r'^audit_detail/$', views.audit_detail, name='audit_detail'),  # 审核订单
    url(r'^settlement_detail/$', views.settlement_detail, name='settlement_detail'),  # 审核订单




]
