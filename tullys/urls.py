from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('', views.home, name='home'),
    path('member_index', views.member_index, name = 'member_index'),
    path('member_new', views.member_new, name = 'member_new'),
    path('shift_index', views.shift_index, name = 'shift_index'),
    path("<int:member_id>/", views.member_detail, name="member_detail"),
    path("<int:member_id>/edit/", views.member_edit, name="member_edit"),
    path("<int:member_id>/member_delete", views.member_delete, name="member_delete"),
    path("<int:member_id>/shift", views.member_shift, name="member_shift"),
    path("<int:member_id>/shift_delete", views.shift_delete, name="shift_delete"),
    path('shift_input', views.shift_input, name = 'shift_input'),
    path('upload', views.upload, name = 'upload'),
] 