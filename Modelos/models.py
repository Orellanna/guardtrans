from asyncio import FastChildWatcher
from pyexpat import model
from re import M
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    tipo_user=models.IntegerField(null=False, default=0)
    nombre_empresa = models.CharField(max_length=100)
    nacionalidad_empresa = models.CharField(max_length=100)
    fechaingreso_empresa = models.DateField()
    registro_empresa=models.CharField(max_length=50, null=False, default='Sin Confirmacion')
    usuario_empresa = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        ordering=["id_empresa"]


class Mercancia(models.Model):
    id_mercancia = models.AutoField(primary_key=True)
    placa_vehiculo = models.ForeignKey('Vehiculo', db_column='placa_vehiculo', blank=True, null=True,on_delete=models.CASCADE)
    nombre_mercancia = models.CharField(max_length=100, null=False, default='Desconocido')
    descripcion_mercancia = models.CharField(max_length=100)
    peso_mercancia = models.FloatField(null=False, default=0.0)
    precio_mercancia = models.FloatField(null=False, default=0.0)  # This field type is a guess.
    tipo_producto_mercancia = models.CharField(max_length=100)
    clasificacion_mercancia = models.CharField(max_length=100)
    class Meta:
        ordering = ["id_mercancia"]


class RegistroAduanero(models.Model):
    id_registro = models.AutoField(primary_key=True)
    id_viajero = models.ForeignKey('Viajero', db_column='id_viajero', blank=True, null=True,on_delete=models.CASCADE)
    carga_registro = models.ForeignKey('Mercancia', db_column='id_mercancia', default=0,on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    reg_registro = models.BooleanField(default=False)
    estado_registro = models.BooleanField(default=False)
    anotaciones_registro = models.CharField(max_length=200)

    class Meta:
        ordering = ["id_registro"]


class Vehiculo(models.Model):
    id_viajero = models.ForeignKey('Viajero', db_column='id_viajero', blank=True, null=True,on_delete=models.CASCADE)
    placa_vehiculo = models.CharField(primary_key=True, max_length=50)
    modelo_vehiculo = models.CharField(max_length=100)
    marca_vehiculo = models.CharField(max_length=100)
    nacionalidad_vehiculo = models.CharField(max_length=100)
    color_vehiculo = models.CharField(max_length=100)

    class Meta:
        ordering = ["placa_vehiculo"]


class Viajero(models.Model):
    id_viajero = models.AutoField(primary_key=True)
    id_empresa = models.ForeignKey(Empresa, db_column='id_empresa', blank=True, null=True,on_delete=models.CASCADE)
    tipo_user=models.IntegerField(null=False, default=0)
    nombre_viajero = models.CharField(max_length=100)
    apellido_viajero = models.CharField(max_length=100)
    fachanaci_viajero = models.DateField()
    cargo_viajero=models.CharField(max_length=50, default='Sin Cargo')
    usuario_viajero = models.ForeignKey(User,on_delete=models.CASCADE)
    nacionalidad_viajero = models.CharField(max_length=100, null=False, default='desconocida')
    identificacion_viajero=models.CharField(max_length=50, null=False, default='desconocida')
    tipo_identificacion=models.CharField(max_length=50, null=False, default='desconocida')
    class Meta:
        ordering = ["id_viajero"]

class Aduanero(models.Model):
    id_aduanero = models.AutoField(primary_key=True)
    nombre_aduanero = models.CharField(max_length=100)
    apellido_aduanero = models.CharField(max_length=100)
    tipo_user=models.IntegerField(null=False, default=0)
    fachanaci_aduanero = models.DateField()
    cargo_aduanero = models.CharField(max_length=100)
    nacionalidad_aduanero = models.CharField(max_length=100)
    usuario_aduanero = models.ForeignKey(User,on_delete=models.CASCADE)
    dui_aduanero = models.CharField(max_length=20)
    class Meta:
        ordering = ["id_aduanero"]

