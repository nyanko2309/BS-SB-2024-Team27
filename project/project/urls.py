
from django.contrib import admin


from . import views
from project.views import login_page, profile
from django.urls import path,include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", login_page, name="login_page"),
    path("profile/", profile, name="profile"),
    path('save_profile_changes/', views.save_profile_changes, name='save_profile_changes'),
    path('login_button/', views.login_button, name='login_button'),
    path('homepage/', views.homepage, name='homepage'),
    path('submit/', views.submit, name="submit"),
    path('register/', views.register, name="register"),
    path('myposts/', views.myposts, name="myposts"),
    path('myfavorites/', views.myfavorites, name="myfavorites"),
    path('helppage/', views.helppage, name="helppage"),
    path('TOS/', views.TOS, name="TOS"),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('create_post/', views.create_post, name="create_post"),
    path('create_post_button/', views.create_post_button, name="create_post_button"),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('remove_post/<int:post_id>/', views.remove_post, name='remove_post'),
    path('rating/', views.rating, name='rating'),
]




