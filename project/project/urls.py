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


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", login, name="login"),
    path("profile/", profile, name="profile"),
    path('create_post/', create_post, name='create_post'),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('login_button/', views.login_button, name='login_button'),
    path('homepage/', views.homepage, name='homepage'),
    path('submit/', views.submit, name="submit"),
    path('register/', views.register, name="register"),
    path('myposts/', views.myposts, name="myposts"),
    path('helppage/', views.helppage, name="helppage"),
    path('TOS/', views.TOS, name="TOS"),
]




