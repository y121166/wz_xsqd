# -*- coding:utf-8 -*-
# @Time    :2018-10-24 10:33
# @Author  :于厚良
# @Email   :yu_houliang@163.com
# @File    :menu.py
# @Software:PyCharm
from rbac.models import Role, Permission
from django.db.models import Q


def role_all_tree(request):
    """
    获取权限树形值
    :return: data
    """

    global role_list
    role_tree_list = []
    per_id = request.POST.get("per_id")

    # 获取权限
    try:
        # 1、获取所有的角色列表
        role_list = Role.objects.filter().values("id", "title")
        # 2、选中角色
        role_check_list = Role.objects.filter(permissions__id=per_id).values("id")
    except Exception as e:
        print(e)
    role_checkList = []
    for role_check_key in role_check_list:
        role_checkList.append(role_check_key["id"])

    for role_key in role_list:
        if role_key["id"] in role_checkList:
            role_tree_list.append({"name": role_key["title"], "id": role_key["id"], "checked": "true"})
        else:
            role_tree_list.append({"name": role_key["title"], "id": role_key["id"], "checked": "false"})
        # print("--------%s" % role_tree_list)
    return role_tree_list


class RoleDeal:

    def __init__(self, request):
        self.role_id = request.POST.get("role_id")  # 角色id
        self.title = request.POST.get("title")  # 角色的名称
        self.response_data = {}

    # 添加角色
    def role_add(self):

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "权限名称不能为空"
            return self.response_data

        # 1、目录 title是否存在
        role_obj = Role.objects.filter(title=self.title).first()
        if role_obj:
            self.response_data["result"] = 'false'
            self.response_data["message"] = "添加角色失败！权限名称已存在！"
            return self.response_data

        # 2、不存在，添加至数据库
        else:
            try:
                Role.objects.create(title=self.title)
                self.response_data["result"] = 'true'
                self.response_data["message"] = "角色添加完成！"
            except Exception as e:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "角色添加失败，未知错误！"
                print(e)

            return self.response_data

    # 修改菜单或权限
    def role_edit(self):

        role_data = {}  # 修改值

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "角色名称不能为空！"
            return self.response_data

        # 1、目录 title是否存在
        role_obj = Role.objects.filter(id=self.role_id).first()
        role_data["title"] = self.title

        if role_obj:
            try:

                Role.objects.filter(id=self.role_id).update(**role_data)
                self.response_data["result"] = 'true'
                self.response_data["message"] = "角色：%s,修改完成！" % self.title
            except Exception as e:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "角色：%s,修改失败，未知错误！" % self.title
                print(e)
            return self.response_data

        # 2、不存在，添加至数据库
        else:
            self.response_data["result"] = 'false'
            self.response_data["message"] = "角色：%s,不存在，请先新增！" % self.title
            return self.response_data

    # 删除角色
    def role_del(self):

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "角色名称不能为空"
            return self.response_data

        # 1、目录 title是否存在
        role_obj = Role.objects.filter(id=self.role_id).first()
        if role_obj:
            try:
                Role.objects.filter(id=self.role_id).delete()
                self.response_data["result"] = 'true'
                self.response_data["message"] = "角色：%s,已删除！" % self.title
            except Exception as e:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "角色：%s,删除失败，未知错误！" % self.title
                print(e)
            return self.response_data

        # 2、不存在，添加至数据库
        else:
            self.response_data["result"] = 'false'
            self.response_data["message"] = "角色：%s,不存在！" % self.title
            return self.response_data


class RolePerDeal:
    """
    权限增加与删除角色
    """

    def __init__(self, per_id, role_id):
        self.per_id = per_id
        self.role_id = role_id
        self.response_data = {}

    # 新增权限-角色对应关系
    def role_per_add(self):

        # 1、操作数据库
        try:
            per_obj = Permission.objects.get(id=self.per_id)
            role_obj = Role.objects.filter(id__in=self.role_id)

            per_obj.role_set.add(*role_obj)
            return True
        except Exception as e:
            print(e)
            return False

    # 删除权限-角色对应关系
    def role_per_del(self):

        # 1、操作数据库
        try:
            per_obj = Permission.objects.get(id=self.per_id)
            role_obj = Role.objects.filter(id__in=self.role_id)

            per_obj.role_set.remove(*role_obj)
            return True
        except Exception as e:
            print(e)
            return False
