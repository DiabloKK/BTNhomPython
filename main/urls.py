from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('profile/', views.profile),
    path('sinhviens/', views.sinhviens),
    path('sinhviens/add/', views.add_sinhvien),
    path('sinhviens/<int:id>/', views.sinhvien_detail),
    path('sinhviens/<int:id>/update/', views.update_sinhvien),
    path('nhanviens/', views.nhanViens, name='nhanViens'),
    path('nhanvien/save', views.nhanVien_save),
    path('nhanvien/<int:id>/', views.nhanVien, name='nhanVien'),
    path('nhanvien/delete/<int:id>/', views.nhanVien_delete),
    path('nhanvien/changepassword/',views.change_password,name ='change_password'),
    path('hopdong/', views.all_constracts),
    path('hopdong_searched', views.search_constracts),
    path('themhopdong/', views.add_constract),
    path('suahopdong/<int:id>/', views.edit_constract),
    path('hopdong_saved', views.constract_saved),
    path('hopdong_delete/<int:id>/', views.delete_constract),
    path('phong/', views.phong, name='phong'),
    path('phong/<int:id>/', views.update_phong, name='update_phong'),
    path('phong/add_Phong', views.add_Phong, name='Add_phong'),
]
