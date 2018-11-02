# -*- coding:utf-8 -*-
# @Time    :2018-10-24 10:33
# @Author  :于厚良
# @Email   :yu_houliang@163.com
# @File    :menu.py
# @Software:PyCharm
from rbac.models import Menu, Permission
from django.db.models import Q, ProtectedError


def menu_all_tree(request):
    """
    获取菜单树形值
    :return: data
    """

    global menu_list, permission_list
    menu_tree_list = []
    only_menu = request.POST.get("only_menu")
    # print("-----------%s" % only_menu)

    # 获取权限
    if only_menu == 'true':
        try:
            # 1、获取所有的菜单列表
            menu_list = list(
                Menu.objects.filter().values("id", "title", "parent_id"))
        except Exception as e:
            print(e)

        for menu_key in menu_list:
            menu_tree_list.append(
                {"name": menu_key["title"], "fieldType": "menu", "id": menu_key["id"], "open": True,
                 "pid": menu_key["parent_id"]})
    # 获取菜单
    else:
        try:
            # 1、获取所有的菜单列表
            menu_list = list(
                Menu.objects.filter().values("id", "title", "parent_id"))
            # 2、获取所有的权限列表
            permission_list = list(
                Permission.objects.filter().values("id", "title", "url", "menu_id", "is_menu")
            )
            print(permission_list)
        except Exception as e:
            print(e)

        # 格式化数据
        for menu_key in menu_list:
            menu_tree_list.append(
                {"id": menu_key["id"], "name": menu_key["title"], "menu_name":menu_key["title"], "pid": menu_key["parent_id"],
                 "fieldType": "menu", "open": True})

        for per_key in permission_list:
            menu_tree_list.append(
                {"name": per_key["title"], "per_name": per_key["title"], "fieldType": "per", "per_id": per_key["id"], "pid": per_key["menu_id"],
                 "perUrl": per_key["url"], "is_menu": per_key["is_menu"]})

    return menu_tree_list


class MenuDeal:

    def __init__(self, request):
        self.title = request.POST.get("title")
        self.menu_id = request.POST.get("id")
        self.pid = request.POST.get("pid")
        self.per_url = request.POST.get("perUrl")
        if request.POST.get("is_menu") == 'true':
            self.is_menu = True
        else:
            self.is_menu = False
        self.response_data = {}

    # 添加菜单或权限
    def menu_add(self):

        menu_data = {}

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "菜单名称不能为空"
            return self.response_data

        if self.per_url == "":  # memu菜单
            # 1、目录 title是否存在
            menu_obj = Menu.objects.filter(title=self.title).first()
            menu_data["title"] = self.title

            if self.pid:
                menu_data["parent_id"] = self.pid

            if menu_obj:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "菜单名称不能重复！"
                return self.response_data

            # 2、不存在，添加至数据库
            else:
                try:
                    Menu.objects.create(**menu_data)
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "菜单添加完成！"
                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "菜单添加失败，未知错误！"
                    print(e)

                return self.response_data
        else:  # per权限
            # 1、目录 title是否存在
            per_obj = Permission.objects.filter(Q(title=self.title) | Q(url=self.per_url)).first()
            if per_obj:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "菜单名称或URL重复！"
                return self.response_data

            # 2、不存在，添加至数据库
            else:
                try:
                    Permission.objects.create(title=self.title, menu_id=self.pid, url=self.per_url,
                                              is_menu=self.is_menu)
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "权限添加完成！"

                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "权限添加失败，未知错误！"
                    print(e)
                return self.response_data

    # 修改菜单或权限
    def menu_edit(self):

        menu_data = {}

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "菜单名称不能为空"
            return self.response_data

        if self.per_url == "":  # memu菜单
            # 1、目录 title是否存在
            menu_obj = Menu.objects.filter(id=self.menu_id).first()
            menu_data["title"] = self.title
            if self.pid:
                menu_data["parent_id"] = self.pid

            if menu_obj:
                try:

                    Menu.objects.filter(id=self.menu_id).update(**menu_data)
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "%s,修改完成！" % self.title
                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "%s,修改失败，未知错误！" % self.title
                    print(e)
                return self.response_data

            # 2、不存在，添加至数据库
            else:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "%s,不存在，请先新增！" % self.title
                return self.response_data
        else:  # per权限
            # 1、目录 title是否存在
            per_obj = Permission.objects.filter(id=self.menu_id).first()
            # print(per_obj)
            if per_obj:
                try:
                    Permission.objects.filter(id=self.menu_id).update(title=self.title, url=self.per_url,
                                                                      is_menu=self.is_menu,
                                                                      menu_id=self.pid)
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "%s,修改完成！" % self.title
                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "%s,修改失败，未知错误！" % self.title
                    print(e)
                return self.response_data

            # 2、不存在
            else:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "%s,不存在，请添加！" % self.title
                return self.response_data

    # 删除菜单或权限
    def menu_del(self):

        if self.title == "":
            self.response_data["result"] = 'false'
            self.response_data["message"] = "菜单名称不能为空"
            return self.response_data

        if self.per_url == "":  # memu菜单

            # 1、目录 title是否存在
            menu_obj = Menu.objects.filter(id=self.menu_id).first()

            if menu_obj:
                try:
                    Menu.objects.filter(id=self.menu_id).delete()
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "%s,已删除！" % self.title
                except ProtectedError:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "%s,下包含子节点，不能删除！" % self.title
                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "%s,删除失败，未知错误！" % self.title
                    print(e)
                return self.response_data

            # 2、不存在，添加至数据库
            else:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "%s,不存在！" % self.title
                return self.response_data
        else:  # per权限
            # 1、目录 title是否存在
            per_obj = Permission.objects.filter(id=self.menu_id).first()
            # print(per_obj)
            if per_obj:
                try:
                    Permission.objects.filter(id=self.menu_id).delete()
                    self.response_data["result"] = 'true'
                    self.response_data["message"] = "%s,已删除！" % self.title
                except Exception as e:
                    self.response_data["result"] = 'false'
                    self.response_data["message"] = "%s,删除失败，未知错误！" % self.title
                    print(e)
                return self.response_data

            # 2、不存在
            else:
                self.response_data["result"] = 'false'
                self.response_data["message"] = "%s,不存在！" % self.title
                return self.response_data
