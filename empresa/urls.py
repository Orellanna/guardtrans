from django.urls import path
from . import views

urlpatterns = [
    path('initempresa', views.init_empresa, name = 'Init_Empresa'),
    path('initempresa/infoup', views.empresa_update, name='Empresa_Update'), 
    path('admingestion', views.admin_aduanero, name='adminAduanero'),    
    path('admingestion/registro', views.registro_aduanero, name='adminAduanero'),
    path('admingestion/info', views.adunero_info, name='info_gestion'),
    path('logout', views.salir, name='salir')
]
