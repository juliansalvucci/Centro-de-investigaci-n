from django.urls import path
from . import views

app_name = 'reservaRT'

urlpatterns = [
    path('', views.opcionReservaTurnoRecursoTecnologico), # Vista para la opcion de reserva de turno de recurso tecnologico
]