from asyncio import sleep
from datetime import datetime, timedelta
import email
import pyautogui, webbrowser
from re import template
from turtle import settiltangle
from django.utils.dateparse import parse_datetime
from multiprocessing import context
from operator import attrgetter
from django.shortcuts import render
from pytz_deprecation_shim import UTC
from centroInvestigacion import settings
from reservaRT.models import CambioEstadoTurno, CentroInvestigacion, Estado, RecursoTecnologico, Sesion, TipoRecursoTecnologico, Turno
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

#GestorReservaTurnoRecursoTecnologico
def mostrarTiposRecursosTecnologicosParaSeleccion(request): # Vista para la opcion de reserva de turno de recurso tecnologico

    tiposRecursosTecnologicos = buscarTiposRecursosTecnologicos() # Obtengo los tipos de recursos tecnologicos

    context = { # Creo el contexto
        'tiposRecursosTecnologicos': tiposRecursosTecnologicos, # Agrego los tipos de recursos tecnologicos
    }

    return render(request, 'Paso1.html', context) # Renderizo la pagina


def buscarTiposRecursosTecnologicos(): # Funcion para buscar los tipos de recursos tecnologicos
    tiposRecursosTecnologicos = [] # Creo una lista para los tipos de recursos tecnologicos
    for tipos in TipoRecursoTecnologico.objects.all(): # Recorro todos los tipos de recursos tecnologicos
        tiposRecursosTecnologicos.append(tipos.getNombre()) # Agrego el nombre del tipo de recurso tecnologico a la lista
    
    return tiposRecursosTecnologicos # Retorno la lista de tipos de recursos tecnologicos


def tomarSeleccionTipoRecursoTecnologico(request): # Funcion para tomar la seleccion del tipo de recurso tecnologico
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado'] # Tomo el tipo de recurso tecnologico seleccionado
    recursosTecnologicos = ordenarPorCI(BuscarRecursosTecnologico(tipoRecursoTecnologicoSeleccionado)) # Busco los recursos tecnologicos del tipo seleccionado y los ordenos por centro de investigación.

    print(recursosTecnologicos,'AAAAHHHH')
    
    context = {
        'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
        'recursosTecnologicos' : recursosTecnologicos,
    }

    return render(request, 'Paso2.html', context)

def BuscarRecursosTecnologico(tipoRT): # Funcion para buscar los recursos tecnologicos de un tipo especifico
    recursosTecnologicos = [] # Creo una lista para los recursos tecnologicos
    for recursoTecnologico in RecursoTecnologico.objects.all(): # Recorro todos los recursos tecnologicos
        if recursoTecnologico.esTuTipoRt(tipoRT): # Si el recurso tecnologico es del tipo seleccionado
            if recursoTecnologico.esReservable(): # Si el recurso tecnologico es reservable
                objRecurso = { 
                   'numeroInventario': recursoTecnologico.getNumeroInventario(),
                   'modelo' : recursoTecnologico.getModelo(),
                   'marca': recursoTecnologico.getMarca(),
                   'centroInvestigacion': recursoTecnologico.getCentroInvestigacion(),
                   'estado': recursoTecnologico.getEstado(),
                }
                recursosTecnologicos.append(objRecurso)

    return recursosTecnologicos # Retorno la lista de recursos tecnologicos

def ordenarPorCI(recursosTecnologicos): # Funcion para ordenar los recursos tecnologicos por centro de investigacion
    recursosOrdenadosPorCI = sorted(recursosTecnologicos, key=lambda k: k['centroInvestigacion']) # Ordeno los recursos tecnologicos por centro de investigacion
    return recursosOrdenadosPorCI


def tomarSeleccionRecursoTecnologico(request): # Funcion para tomar la seleccion del recurso tecnologico
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado'] # Tomo el recurso tecnologico seleccionado
    rtSeleccionado = RecursoTecnologico.objects.get(numeroRT=recursoTecnologicoSeleccionado) # Busco el recurso tecnologico seleccionado
    cientificoLogueado = buscarCientificoLogueado(1) # Busco el cientifico logueado

    if not rtSeleccionado.validarCientifico(cientificoLogueado): # Si el cientifico logueado no pertenece al mismo centro del recurso tecnologico seleccionado.
        context = {
            'error': 'El cientifico logueado no es el mismo que el que reserva el recurso tecnologico',
        }
        return render(request, 'Paso6.html', context)

   
    print(cientificoLogueado)

    context = {
        'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
        'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
        'cientificoLogueado': cientificoLogueado,
    }

    return render(request, 'Paso3.html', context)

def buscarCientificoLogueado(sesion): # Funcion para buscar el cientifico logueado.
    activaSesion = Sesion.objects.get(pk=sesion) # Busco la sesion activa.
    cientificoLoqueado = activaSesion.getUsuarioEnSesion() # Busco el cientifico logueado.
    return cientificoLoqueado

def validarCientificoDeRecursoTecnologico(request): # Funcion para validar el cientifico de un recurso tecnologico.
    cientificoLogueado = request.POST['cientificoLogueado'] # Tomo el cientifico logueado.
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado'] # Tomo el recurso tecnologico seleccionado.

    recursoTecnologicoSeleccionado.validarCientifico(cientificoLogueado) # Valido el cientifico del recurso tecnologico.
    
def mostrarTurnosDeRecursoTecnologico(request):
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado']
    cientificoLogueado = request.POST['cientificoLogueado']
    rtSeleccionado = RecursoTecnologico.objects.get(numeroRT=recursoTecnologicoSeleccionado)
    print(recursoTecnologicoSeleccionado)
    turnosDeRecursoTecnologico = getTurnosDeRecursoTecnologico(rtSeleccionado)
  
    if len(turnosDeRecursoTecnologico) == 0:
        context = {
            'error': 'No hay turnos para el recurso tecnologico seleccionado',
        }
        return render(request, 'Paso7.html', context)

    print(turnosDeRecursoTecnologico)

    context = {
        'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
        'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
        'turnosDeRecursoTecnologico': turnosDeRecursoTecnologico,
        'cientificoLogueado': cientificoLogueado,
    }

    return render(request, 'Paso4.html', context)

def getFechaHoraActual():
    return datetime.now()

def getTurnosDeRecursoTecnologico(recursoTecnologicoSeeccionado):
    turnos = recursoTecnologicoSeeccionado.getTurnos()
    turnosParaSeleccion = []
    fechaHoraActual = getFechaHoraActual()
    for turno in turnos:
        if turno.getFechaHoraInicio().replace(tzinfo=UTC) > fechaHoraActual.replace(tzinfo=UTC): # Si el turno no ha comenzado
           objTurno = {
               'fechaGeneracion' : turno.getFechaGeneracion(),
               'diaSemana': turno.getDiaSemana(),
               'fechaHoraInicio' : turno.getFechaHoraInicio(),
               'fechaHoraFin' : turno.getFechaHoraFin(),
               'estado': turno.getEstado()
           }
           turnosParaSeleccion.append(objTurno)
       
    return turnosParaSeleccion
    
def tomarSeleccionTurno(request):
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado']
    cientificoLogueado = request.POST['cientificoLogueado']
    turnoSeleccionado = request.POST['turnoSeleccionado']

    context = {
        'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
        'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
        'turnoSeleccionado': turnoSeleccionado,
        'cientificoLogueado': cientificoLogueado,
        'turnoSeleccionado': turnoSeleccionado,
    }

    return render(request, 'Paso5.html', context)


def confirmarReserva(request):
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado']
    cientificoLogueado = request.POST['cientificoLogueado']
    turnoSeleccionado = request.POST['turnoSeleccionado']
   
    print(recursoTecnologicoSeleccionado)

    turno = Turno.objects.get(diaSemana=turnoSeleccionado)
    #recursoTecnologico = RecursoTecnologico.objects.get(numeroRT=recursoTecnologicoSeleccionado)

    
    mail = request.POST.get('confirmacionMail','off')

    whatsapp = request.POST.get('confirmacionWhatsapp','off')
    estado = buscarEstadoReservado()

    fechaHoraActual = getFechaHoraActual()
    fechaHoraDesde = (fechaHoraActual).replace(tzinfo=None)
   
    turno.crearNuevoCambioEstadoTurno(fechaHoraDesde,estado)

    
    if mail == 'on':
        enviarMail(request)

    if whatsapp == 'on':
        enviarWP(request)
    

    context ={
       'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
       'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
       'turno': turno,
       #'recursoTecnologico': recursoTecnologico,
       'cientificoLogueado': cientificoLogueado,
       'msg': 'reservaConfirmada'
    }
    return render(request, 'Paso8.html', context)

def buscarEstadoReservado():
    for estado in Estado.objects.all():
        if estado.esAmbitoTurno():
            if estado.mostrarEstado() == "Reservado":
                return estado

def enviarMail(request):
    if request.method == 'POST':
        tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
        turnoSeleccionado = request.POST['turnoSeleccionado']
        turno = Turno.objects.get(diaSemana=turnoSeleccionado)
        mensaje = 'Se ha confirmado la reserva del turno '

        template = render_to_string('Paso8.html', {
            'mensaje': mensaje,
        })

        email = EmailMessage(
            mensaje,
            template,
            settings.EMAIL_HOST_USER,
            ['julianls783@gmail.com']
        )

        email.fail_silently = False
        email.send()


def enviarWP(request):
     if request.method == 'POST':
       webbrowser.open('https://web.whatsapp.com/send?phone=+543535648757')

       sleep(5)
  
       for i in range(2):
         pyautogui.typewrite('Hola')
         pyautogui.press('enter')

    