from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),

    path('phong/',views.phong, name= 'phong'),
    path('phong/<int:id>/',views.update_phong, name= 'update_phong'),
    path('phong/add_Phong',views.add_Phong, name= 'Add_phong'),

    path('nhanviens/', views.nhanViens, name='nhanViens'),
    path('nhanvien/save', views.nhanVien_save),
    path('nhanvien/<int:id>/', views.nhanVien, name='nhanVien'),
    path('nhanvien/delete/<int:id>/', views.nhanVien_delete)

]