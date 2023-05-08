from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),
    path('sinhviens/', views.sinhviens),
    path('sinhviens/add/', views.add_sinhvien),
    path('sinhviens/<int:id>/', views.sinhvien_detail),
    path('sinhviens/<int:id>/update/', views.update_sinhvien),
    path('nhanviens/', views.nhanViens, name='nhanViens'),
    path('nhanvien/save', views.nhanVien_save),
    path('nhanvien/<int:id>/', views.nhanVien, name='nhanVien'),
    path('nhanvien/delete/<int:id>/', views.nhanVien_delete)
]
