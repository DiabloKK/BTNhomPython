from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile/', views.profile),
    path('phong/',views.phong, name= 'phong'),
    path('phong/<int:id>/',views.update_phong, name= 'update'),
    path('phong/add_Phong',views.add_Phong, name= 'Add'),
]