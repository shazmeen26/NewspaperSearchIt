"""Searchingzilla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from accounts.views import *


urlpatterns = [
    path("", home, name="home"),
    path("loginSignup", loginSignup, name="loginSignup"),
    path("upload", upload, name="upload"),
    path("logout", accountLogout, name="logout"),
    path("search", search, name="search"),
    path("approve", listUnapprovedPost, name="unapprovedPost"),
    path("approvePost", csrf_exempt(approvePost), name="approvePost"),
    path("rejectPost", rejectPost, name="rejectPost")
]
