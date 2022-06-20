from django.urls import path
from . import views

urlpatterns = [
    path('adminc', views.admin_cargas, name = 'Admin_Cargas'),
    path('adminc/details', views.detalles_carga, name='Detalles_Carga'), 
    path('adminc/modi', views.modificar_carga, name='Modificar_Carga'),    
    path('adminc/add', views.registrar_cargar, name='Agregar_Carga'),
]