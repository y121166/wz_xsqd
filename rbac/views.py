from django.conf import settings
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect, reverse
from .models import UserInfo, Department, Role, DepField
import json
from rbac.service.init_permission import init_permission
from django.http import JsonResponse
from wzjt.wz_pack.pycrypto import *
from wzjt.wz_pack.auth_login import auth

from rbac.wz_rbac_pack import menu, role


# Create your views here.
# 登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'rbac/login.html')
    else:
        key = PrpCrypt('wzjtwzjtwzjtwzjt') # 密码加密key
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = key.encrypt(password)
        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        if not user_obj:
            return render(request, 'rbac/login.html',
                          {'error': '用户名或密码错误！', 'username': username, 'password': ''})
        else:
            init_permission(request, user_obj)  # 调用init__permission，进行初始化
            request.session['dep_id'] = user_obj.department_id
            request.session['username'] = user_obj.last_name
            request.session['user_id'] = user_obj.id
            request.session['roles_id'] = user_obj.roles_id
            if username == 'admin':
                return redirect('/rbac/index/')
            else:
                return redirect('/wzjt/index/')


# 首页
def index(request):
    return render(request, 'rbac/index.html')


# 退出
@auth
def logout(request):
    request.session.clear()
    # del request.session['username']
    # del request.session[settings.SESSION_PERMISSION_URL_KEY]
    return redirect('/rbac/index/')


# 用户列表
def user_table(request):
    if request.method == "GET":
        user_list = UserInfo.objects.all().values('id',
                                                  'username',
                                                  'last_name',
                                                  'department__title',
                                                  'roles__title')
        return render(request, 'rbac/user_table.html', {"user_list": user_list})
    else:
        username = request.POST.get("username")
        last_name = request.POST.get("last_name")
        dep_select = request.POST.get("dep_select")
        roles_select = request.POST.get("roles_select")
        password = "888888"
        # 密码加密
        key = PrpCrypt('wzjtwzjtwzjtwzjt')
        encrypt_password = key.encrypt(password)
        # print(encrypt_password)
        response_data = {}
        try:
            UserInfo.objects.create(username=username, password=encrypt_password, last_name=last_name, department_id=dep_select,
                                    roles_id=roles_select)
            # TD  进行修改操作
            response_data['result'] = 'true'
            response_data['message'] = '用户添加成功！'
            print('<info>-----%s用户添加成功！' % last_name)
        except Exception as e:
            response_data['result'] = 'false'
            response_data['message'] = '用户添加失败！'
            print(e)
        return JsonResponse(response_data, safe=False)


# 用户列表详情
def user_view(request, nid):
    user_obj = list(
        UserInfo.objects.filter(id=nid).all().values('id', 'username', 'password', 'last_name', 'department', 'roles'))
    print()
    response_data = {}
    try:
        response_data['result'] = 'Success'
        response_data['userinfo'] = json.dumps(user_obj, ensure_ascii=False)
    except Exception as e:
        response_data['result'] = 'Ouch!'
        print(e)
    # print(response_data)
    return JsonResponse(response_data, safe=False)


# 用户修改保存URL
@auth
def user_Edit(request):
    id = request.POST.get("id")
    last_name = request.POST.get("last_name")
    dep_select = request.POST.get("dep_select")
    roles_select = request.POST.get("roles_select")
    response_data = {}
    try:
        UserInfo.objects.filter(id=id).update(last_name=last_name, department=dep_select, roles=roles_select)
        # TD  进行修改操作
        response_data['result'] = 'true'
        response_data['message'] = '用户修改成功！'
    except Exception as e:
        response_data['result'] = 'false'
        response_data['message'] = '用户修改失败！'

    return JsonResponse(response_data, safe=False)


# 用户删除URL
@auth
def user_del(request, nid):
    id = nid
    response_data = {}
    try:
        UserInfo.objects.filter(id=id).delete()
        response_data['result'] = 'true'
        response_data['message'] = '用户删除成功！'
    except Exception as e:
        response_data['result'] = 'false'
        response_data['message'] = '用户删除失败！'

    return JsonResponse(response_data, safe=False)


# 部门列表
def dep_table(request):
    if request.method == "GET":
        dep_list = Department.objects.all().values('id', 'title', 'dep_code')
        return render(request, 'rbac/dep_table.html', {"dep_list": dep_list})
    else:
        title = request.POST.get("title")
        dep_code = request.POST.get("dep_code")
        print_str = request.POST.get("print_checkbox_str")
        # print(dep_code)
        response_data = {}

        # 判定title是否存在
        dep_title = Department.objects.filter(title=title).first()
        if dep_title:
            response_data['result'] = 'false'
            response_data['message'] = '部门 “%s” 已存在，请修改！' % title
            return JsonResponse(response_data, safe=False)

        # 判定简写是否存在
        dep_dep_code = Department.objects.filter(dep_code=dep_code).first()
        if dep_dep_code:
            response_data['result'] = 'false'
            response_data['message'] = '部门简写 “%s” 已存在，请修改！' % dep_code
            return JsonResponse(response_data, safe=False)

        try:
            dep_obj = Department.objects.create(title=title, dep_code=dep_code)
            DepField.objects.create(field_str=print_str, department=dep_obj)
            # print(dep_obj.id)
            response_data['result'] = 'true'
            response_data['message'] = '%s 创建完成！' % title
        except Exception as e:
            response_data['result'] = 'false'
            response_data['message'] = '未知错误，请联系管理员!'
            print(e)
        return JsonResponse(response_data, safe=False)


# 部门列表详情
@auth
def dep_view(request, nid):
    dep_obj = list(Department.objects.filter(id=nid).all().values('id', 'title', 'dep_code', 'depfield__field_str'))

    # print(dep_obj)

    response_data = {}
    try:
        response_data['dep_info'] = json.dumps(dep_obj, ensure_ascii=False)
        response_data['result'] = 'Success'
    except Exception as e:
        response_data['result'] = 'Ouch!'
        print(e)
    # print(response_data)
    return JsonResponse(response_data, safe=False)


# 部门修改保存
@auth
def dep_edit(request):
    id = request.POST.get("id")
    title = request.POST.get("title")
    print_str = request.POST.get("print_checkbox_str")
    response_data = {}

    dep_obj = Department.objects.filter(id=id).first()
    if not dep_obj:
        response_data['result'] = 'false'
        response_data['message'] = '%s 不存在，请确认！' % title
        return JsonResponse(response_data, safe=False)

    try:
        Department.objects.filter(id=id).update(title=title)
        DepField.objects.filter(department=id).update(field_str=print_str)
        response_data['result'] = 'true'
        response_data['message'] = '%s 修改完成！' % title
    except Exception as e:
        response_data['result'] = 'false'
        response_data['message'] = '未知错误，请联系管理员！'
        print(e)
    return JsonResponse(response_data, safe=False)


# 部门删除URL
@auth
def dep_del(request, nid):
    id = nid
    response_data = {}
    try:
        Department.objects.filter(id=id).delete()
        response_data['result'] = 'Success'
    except Exception as e:
        response_data['result'] = 'Error'

    return JsonResponse(response_data, safe=False)


# 菜单页面
@auth
def menu_page(request):
    return render(request, 'rbac/menu_table.html')


# 菜单树结构
def menu_tree(request):
    response_data = menu.menu_all_tree(request)  # 获取menu_json
    # print(response_data)
    return JsonResponse(response_data, safe=False)


# 菜单或权限新增
def menu_add(request):
    menu_deal_obj = menu.MenuDeal(request)
    response_data = menu_deal_obj.menu_add()
    return JsonResponse(response_data, safe=False)


# 菜单或权限修改
def menu_edit(request):
    menu_deal_obj = menu.MenuDeal(request)
    response_data = menu_deal_obj.menu_edit()
    return JsonResponse(response_data, safe=False)


# 菜单或权限删除
def menu_del(request):
    menu_deal_obj = menu.MenuDeal(request)
    response_data = menu_deal_obj.menu_del()
    return JsonResponse(response_data, safe=False)


# 角色表
def role_page(request):
    return render(request, 'rbac/role_table.html')


# 角色树结构
def role_tree(request):
    response_data = role.role_all_tree(request)  # 获取role_json
    return JsonResponse(response_data, safe=False)


def role_change(request):
    """
    变更当前权限分配的角色
    :param request:
    :return: response_data
    """
    response_data = {}
    roleNodes_list = json.loads(request.POST["applicants"])  # 反序列化request
    per_id = roleNodes_list["per_id"]
    roleAddNodes_list = roleNodes_list["roleAddNodes_list"]
    roleDelNodes_list = roleNodes_list["roleDelNodes_list"]
    role_del_result = role_add_result = True

    if roleAddNodes_list:
        role_per_deal = role.RolePerDeal(per_id, roleAddNodes_list)
        role_add_result = role_per_deal.role_per_add()

    if roleDelNodes_list:
        role_per_deal = role.RolePerDeal(per_id, roleDelNodes_list)
        role_del_result = role_per_deal.role_per_del()

    if role_add_result and role_del_result:
        response_data["result"] = 'true'
        response_data["message"] = "权限修改完成！"
    else:
        response_data["result"] = 'false'
        response_data["message"] = "权限修改失败，未知错误！"
    return JsonResponse(response_data, safe=False)


def per_role_list(request):
    data = menu.role(request)
    return render(request, 'rbac/role_table.html')


# 初始化select值
def user_init_select(request):
    dep_obj = list(Department.objects.filter().all().values('id', 'title'))  # 部门
    rolse_obj = list(Role.objects.filter().all().values('id', 'title'))  # 角色
    response_data = {}
    try:
        response_data['result'] = 'Success'
        response_data['depinfo'] = json.dumps(dep_obj, ensure_ascii=False)
        response_data['rolesinfo'] = json.dumps(rolse_obj, ensure_ascii=False)
        print("初始化select值成功！")
    except Exception as e:
        response_data['result'] = 'Ouch!'
        print(e)
    return JsonResponse(response_data, safe=False)


# 密码修改
@auth
def edit_psw(request):
    user_id = request.session['user_id']
    req_old_psw = request.POST.get('old_psw')
    new_psw = request.POST.get('new_psw')
    key = PrpCrypt('wzjtwzjtwzjtwzjt')  # 加密key
    response_data = {}

    old_psw = UserInfo.objects.get(id=user_id)
    # old_psw = key.decrypt(old_psw.password)

    if old_psw.password == req_old_psw:
        # 新密码加密
        try:
            new_psw = key.encrypt(new_psw)
            UserInfo.objects.filter(id=user_id).update(password=new_psw)
            del request.session['username']
            del request.session[settings.SESSION_PERMISSION_URL_KEY]
            response_data['result'] = 'true'
            response_data['message'] = '密码修改成功！'
        except Exception as e:
            response_data['result'] = 'false'
            response_data['message'] = '密码修改失败，请联系管理员！'
            print(e)
    else:
        response_data['result'] = 'false'
        response_data['message'] = '原密码不正确，请确认！'
    return JsonResponse(response_data, safe=False)
