from django.urls import path
from . import views

from django.conf.urls import handler404
from basics.views import error404

urlpatterns = [ 
    path('initviajero', views.init_viajero, name = 'InicioSesion_Viajero'),
    path('initviajero/infoup/<str:username>', views.actualizar_viajero, name = 'Actualizar_Viajero'),
    path('adminu/<str:username>', views.admin_viajeros, name='Administrar_Viajeros'),
    path('adminu/details/<str:username>', views.detalles_viajero, name='Detalles_Viajero'),
    path('adminu/modi/<str:username>', views.modificar_viajero, name = 'Modificar_Viajero'),
    #path('logout', views.cerrar_sesion, name='Salir'), 
]

handler404 = error404