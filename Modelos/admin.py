from django.contrib import admin
from .models import Aduanero, Empresa
from .models import Mercancia
from .models import RegistroAduanero
from .models import Vehiculo
from .models import Viajero

# Register your models here.
admin.site.register(Empresa)
admin.site.register(Mercancia)
admin.site.register(RegistroAduanero)
admin.site.register(Vehiculo)
admin.site.register(Viajero)
admin.site.register(Aduanero)