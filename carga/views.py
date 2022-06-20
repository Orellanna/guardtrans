
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from Modelos.models import Vehiculo, Mercancia, RegistroAduanero, Viajero
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url="/login")
def registrar_cargar(request):
    template = loader.get_template('registrarCarga.html')

    placa = request.GET.get('id')

    if request.method == 'POST':
        nom = request.POST['nom']
        descrip = request.POST['desc']
        peso = request.POST['peso']
        precio = request.POST['precio']
        clasif = request.POST['clasif']  

        p = Vehiculo.objects.get( placa_vehiculo = placa)
        newcarga = Mercancia.objects.create(placa_vehiculo = p, nombre_mercancia = nom, descripcion_mercancia = descrip,
            peso_mercancia = peso, precio_mercancia = precio, clasificacion_mercancia = clasif)
        newcarga.save()

        vehi = Vehiculo.objects.filter(placa_vehiculo = placa).first()
        idv = vehi.id_viajero
        idmerca = Mercancia.objects.get( id_mercancia = newcarga.id_mercancia)
    
        registro = RegistroAduanero.objects.create(id_viajero = idv, carga_registro = idmerca,
        fecha_registro = datetime.datetime.now().date(), anotaciones_registro = "")
        registro.save()

        messages.add_message(request=request, level=messages.SUCCESS, message="Carga registrada correctamente!")

    context={}
    return HttpResponse(template.render(context, request))

@login_required(login_url="/login")
def modificar_carga(request):
    template = loader.get_template('modificarCarga.html')

    id = request.GET.get('id')

    if request.method == 'POST':
        nom = request.POST['nom']
        descrip = request.POST['desc']
        peso = request.POST['peso']
        precio = request.POST['precio']
        clasif = request.POST['clasif']

        #la carga se actualiza
        Mercancia.objects.filter(id_mercancia = id).update(nombre_mercancia = nom, descripcion_mercancia = descrip,
        peso_mercancia = peso, precio_mercancia = precio, clasificacion_mercancia = clasif)

    info = Mercancia.objects.filter( id_mercancia = id ).first()

    context={
        'login': request.user, 
        'info': info
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/login")
def detalles_carga(request, placa_vehiculo = None ):
    template = loader.get_template('detallesCarga.html')

    id = request.GET.get('id')
    info = Mercancia.objects.filter(id_mercancia = id ).first()

    context={
        'login': request.user, 
        'info': info
    }

    return HttpResponse(template.render(context, request))


def admin_cargas(request):
    template = loader.get_template('administrarCarga.html')

    num=1
    num=request.GET.get('page')
    busqueda = request.GET.get('search')

    if request.GET.__contains__('search'):  
        busqueda = Mercancia.objects.filter( id_mercancia = busqueda ).values() | Mercancia.objects.filter(nombre_mercancia=busqueda).values() | Mercancia.objects.filter(placa_vehiculo=busqueda).values()
        pagi=Paginator(busqueda,8)
    else:
        #pagi=Paginator(Mercancia.objects.filter( placa_vehiculo = v.placa_vehiculo ).values() ,8)
         pagi=Paginator(Mercancia.objects.all() ,8)
       
    datos=pagi.get_page(num)

    context={
        'login': request.user,
       'paginacion': datos
    }

    return HttpResponse(template.render(context, request))