from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^index/', views.index, name='index'),
    url(r'^role/', views.role_page, name='role'),
    url(r'^menu/', views.menu_page, name='menu'),

    # 用户相关
    url(r'^user/', views.user_table, name='user'),
    url(r'^user_view-(?P<nid>\d+)/$', views.user_view, name='user_view'),
    url(r'^user_Edit/$', views.user_Edit, name='user_Edit'),
    url(r'^user_del-(?P<nid>\d+)/$', views.user_del, name='user_del'),
    url(r'^user_init_select/$', views.user_init_select, name='user_init_select'),
    url(r'^edit_psw/$', views.edit_psw, name='edit_psw'),

    # 部门相关
    url(r'^dep/', views.dep_table, name='dep'),
    url(r'^dep_view-(?P<nid>\d+)/$', views.dep_view, name='dep_view'),
    url(r'^dep_edit/$', views.dep_edit, name='dep_edit'),
    url(r'^dep_del-(?P<nid>\d+)/$', views.dep_del, name='dep_del'),

    # 菜单相关
    url(r'^menu_tree/$', views.menu_tree, name='menu_tree'),
    url(r'^menu_add/$', views.menu_add, name='menu_add'),
    url(r'^menu_edit/$', views.menu_edit, name='menu_edit'),
    url(r'^menu_del/$', views.menu_del, name='menu_del'),
    url(r'^per_role_list/$', views.per_role_list, name='per_role_list'),

    # 角色相关
    url(r'^role_tree/$', views.role_tree, name='role_tree'),
    url(r'^role_change/$', views.role_change, name='role_change'),

]
