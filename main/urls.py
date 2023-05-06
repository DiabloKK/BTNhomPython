from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),
    path('nhanviens/', views.nhanViens, name='nhanViens'),
    path('nhanvien/save', views.nhanVien_save),
    path('nhanvien/<int:id>/', views.nhanVien, name='nhanVien'),
    path('nhanvien/delete/<int:id>/', views.nhanVien_delete)
]