from django.urls import path
from . import views

urlpatterns = [
    path('adminv/<int:username>', views.admin_vehiculo, name = 'Admin_Vehiculo'),
    path('adminv/details', views.details_vehiculo, name='Detalles_vehiculo'), 
    path('adminv/modi', views.update_vehiculo, name='Modificar_vehiculo'),    
    path('adminv/add', views.add_vehiculo, name='Agregar_vehiculo'),
]
