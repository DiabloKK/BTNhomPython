from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),
    path('nhanviens/', views.nhanViens, name='nhanViens'),
    path('nhanvien/save', views.nhanVien_save),
    path('nhanvien/<int:id>/', views.nhanVien, name='nhanVien'),
    path('nhanvien/delete/<int:id>/', views.nhanVien_delete),
    path('hopdong/', views.all_constracts),
    path('hopdong_searched', views.search_constracts),
    path('themhopdong/', views.add_constract),
    path('suahopdong/<int:id>/', views.edit_constract),
    path('hopdong_saved', views.constract_saved),
    path('hopdong_delete/<int:id>/', views.delete_constract)
]