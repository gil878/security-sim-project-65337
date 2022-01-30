"""securityproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path

from loginApp.views import *
# from .sql_handler import testSql

urlpatterns = [
    path('',login_view),
    path('system/',login_required(system_view)),
    path('register/',register_view),
    path('forgot/',forgot_view),
    path('forgot/change_password/<str:email>/',forgot_change_pass_view),
    path('system/change_password/',login_required(change_pass_view)),
    path('admin/', admin.site.urls),
    #path('accounts/login/',system_view)
]
