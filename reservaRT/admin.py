from django.contrib import admin
from reservaRT.models import *

admin.site.register(TipoRecursoTecnologico) # Registro el modelo TipoRecursoTecnologico
admin.site.register(Usuario)
admin.site.register(RecursoTecnologico)
admin.site.register(Sesion)
admin.site.register(Modelo)
admin.site.register(Marca)
admin.site.register(CentroInvestigacion)
admin.site.register(AsignacionCientificoDelCI)
admin.site.register(PersonalCientifico)
admin.site.register(CambioEstadoRT)
admin.site.register(Turno)
admin.site.register(CambioEstadoTurno)
admin.site.register(Estado)