from django.contrib import admin
from reservaRT.models import *

admin.site.register(TipoRecursoTecnologico) # Registro el modelo TipoRecursoTecnologico
admin.site.register(Usuario)
admin.site.register(RecursoTecnologico)
admin.site.register(Sesion)
admin.site.register(Modelo)
admin.site.register(Marca)
admin.site.register(CentroInvestigacion)