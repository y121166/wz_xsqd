"""
Django settings for wz_xsqd project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1l9d!=qqwodf##j)+$0lr=s#7@lyr7r78*x%&&um1a$anci0k!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wzjt.apps.XsqdConfig',
    'rbac',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middleware.rbac.RbacMiddleware'  # 加入自定义的中间件到最后
]

ROOT_URLCONF = 'wz_xsqd.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',  # 添加static
            ],
        },
    },
]

WSGI_APPLICATION = 'wz_xsqd.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wzxsqd',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# session设置
SESSION_COOKIE_AGE = 60 * 60  # 失效时间
SESSION_SAVE_EVERY_REQUEST = True  # 超时时间按照每次访问之后开启计算
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 关闭浏览器，则COOKIE失效

# 定义session 键：
# 保存用户权限url列表
# 保存 权限菜单 和所有 菜单
SESSION_PERMISSION_URL_KEY = 'cool'

SESSION_MENU_KEY = 'awesome'
ALL_MENU_KEY = 'k1'
PERMISSION_MENU_KEY = 'k2'

LOGIN_URL = '/rbac/login/'

REGEX_URL = r'^{url}$'

# 配置url权限白名单
SAFE_URL = [
    # r'/myapp/login/',
    # '/myapp/index/',
    # '/myadmin/.*',
    # '/test/',
    # '/rbac/index/',

    # 后台
    '/rbac/login/',  # 登录
    '/rbac/logout/',  # 退出
    '/rbac/user_init_select/',  # 返回部门、角色select数据
    '/rbac/user_Edit/',  # 用户修改
    '/rbac/user_del-(?P<nid>\d+)/',  # 用户删除
    '/rbac/user_view-(?P<nid>\d+)/',  # 用户详情
    '/rbac/edit_psw/',  # 修改密码
    '/rbac/dep_edit/',  # 部门修改
    '/rbac/dep_del-(?P<nid>\d+)/',  # 部门删除
    '/rbac/dep_view-(?P<nid>\d+)/',  # 部门详情

    # 角色、菜单、权限相关url
    '/rbac/menu/',  # 菜单页
    '/rbac/menu_tree/',  # 菜单树
    '/rbac/menu_add/',  # 菜单增加
    '/rbac/menu_edit/',  # 菜单修改
    '/rbac/menu_del/',  # 菜单删除

    '/rbac/role/',
    '/rbac/role_tree/',  # 角色树
    '/rbac/per_role_list/',  # 权限
    '/rbac/role_change/',  # 权限

    # 前台
    '/wzjt/return_car_list/',  # 返回车辆列表
    '/wzjt/return_detail_list/',  # 返回订单列表
    '/wzjt/add_vehicle/',  # 添加车辆信息
    '/wzjt/edit_vehicle/',  # 修改车辆信息
    '/wzjt/del_vehicle/',  # 删除车辆信息
    '/wzjt/vehicle_info-(?P<nid>\d+)/',  # 车辆详情
    '/wzjt/vehicle_import/',  # 车辆导入
    '/wzjt/vehicle_down/',  # 车辆导入模板下载
    '/wzjt/get_vehicle_vin/',  # 返回车辆VIN，订单填写VIN使用
    '/wzjt/add_detail/',  # 新增订单
    '/wzjt/edit_detail/',  # 修改订单
    '/wzjt/info_detail-(?P<nid>\d+)/',  # 订单详情
    '/wzjt/withdraw_detail/',  # 撤回订单
    '/wzjt/del_detail/',  # 删除订单
    '/wzjt/audit_detail/',  # 审核订单
    '/wzjt/settlement_detail/',  # 结算订单


   # '/wzjt/.*',
   # '^/rbac/',
]

# 启用日志中心
BASE_LOG_DIR = os.path.join(BASE_DIR, "log")

# LOGGING = {
# #     'version': 1,
# #     'disable_existing_loggers': False,
# #     'filters': {
# #         'require_debug_true': {
# #             '()': 'django.utils.log.RequireDebugTrue',
# #         },  # 针对 DEBUG = True 的情况
# #     },
# #     'formatters': {
# #         'standard': {
# #             'format': '%(levelname)s %(asctime)s %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d: %(message)s'
# #         },  # 对日志信息进行格式化，每个字段对应了日志格式中的一个字段，更多字段参考官网文档，我认为这些字段比较合适，输出类似于下面的内容
# #         # INFO 2016-09-03 16:25:20,067 /home/ubuntu/mysite/views.py views.py views get 29: some info...
# #     },
# #     'handlers': {
# #         'mail_admins': {
# #             'level': 'ERROR',
# #             'class': 'django.utils.log.AdminEmailHandler',
# #             'formatter': 'standard'
# #         },
# #         'file_handler': {
# #             'level': 'DEBUG',
# #             'class': 'logging.handlers.TimedRotatingFileHandler',
# #             'filename': os.path.join(BASE_LOG_DIR, "xxx_admin.log"),
# #             'formatter': 'standard'
# #         },  # 用于文件输出
# #         'console': {
# #             'level': 'INFO',
# #             'filters': ['require_debug_true'],
# #             'class': 'logging.StreamHandler',
# #             'formatter': 'standard'
# #         },
# #     },
# #     'loggers': {
# #         'django': {
# #             'handlers': ['file_handler', 'console'],
# #             'level': 'DEBUG',
# #             'propagate': True  # 是否继承父类的log信息
# #         },  # handlers 来自于上面的 handlers 定义的内容
# #         'django.request': {
# #             'handlers': ['mail_admins'],
# #             'level': 'ERROR',
# #             'propagate': False,
# #         },
# #     }
# # }
