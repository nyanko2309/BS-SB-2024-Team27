"""
URL configuration for jobs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from posts.views import create_post

from . import views
from .views import login, profile
from django.urls import path,include
from login.views import register, registration_success

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
    path("register/", register, name="register"),
    path('create_post/', create_post, name='create_post'),
    path("register/", register, name="register"),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('login_button/', views.login_button, name='login_button'),
    path('registration_success/', registration_success, name='registration_success'),
]




