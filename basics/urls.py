from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_r, name='login'),
    path('contactanos', views.contactanos, name='contactos'),
    path('newviajero/', views.registrar_viajero, name = 'Registrar_Viajero'),
    path('error', views.error404, name='ERROR'),
    path('newempresa/', views.registrar_empresa, name = 'Registrar_Empresa'),
    path('adminempresa/add/<str:username>', views.re_viajero, name = 'Rempresa_Viajero'),
]
