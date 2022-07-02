from django.urls import path
from . import views

app_name = 'reservaRT'

urlpatterns = [
    path('', views.mostrarTiposRecursosTecnologicosParaSeleccion), # Vista para la opcion de reserva de turno de recurso tecnologico
    path('tomarSeleccionTipoRecursoTecnologico/', views.tomarSeleccionTipoRecursoTecnologico), # Vista para la opcion de reserva de turno de recurso tecnologico
    path('tomarSeleccionRecursoTecnologico/', views.tomarSeleccionRecursoTecnologico), # Vista para la opcion de reserva de turno de recurso tecnologico
    path('mostrarTurnosDeRecursoTecnologico/',views.mostrarTurnosDeRecursoTecnologico),
    path('tomarSeleccionTurno/', views.tomarSeleccionTurno),
]