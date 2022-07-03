import datetime
from multiprocessing import context
from operator import attrgetter
from django.shortcuts import render
from reservaRT.models import CentroInvestigacion, Estado, RecursoTecnologico, Sesion, TipoRecursoTecnologico

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
                }
                recursosTecnologicos.append(objRecurso)

    return recursosTecnologicos # Retorno la lista de recursos tecnologicos

def ordenarPorCI(recursosTecnologicos): # Funcion para ordenar los recursos tecnologicos por centro de investigacion
    recursosOrdenadosPorCI = sorted(recursosTecnologicos, key=lambda k: k['centroInvestigacion']) # Ordeno los recursos tecnologicos por centro de investigacion
    return recursosOrdenadosPorCI


def tomarSeleccionRecursoTecnologico(request): # Funcion para tomar la seleccion del recurso tecnologico
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado'] # Tomo el recurso tecnologico seleccionado
    rtSeleccionado = RecursoTecnologico.objects.get(numeroRT=recursoTecnologicoSeleccionado) # Busco el recurso tecnologico seleccionado
    cientificoLogueado = buscarCientificoLogueado(1) # Busco el cientifico logueado

    aux = rtSeleccionado.validarCientifico(cientificoLogueado) 

   
    print(cientificoLogueado)
    print(aux, "PerteneceACI")

    context = {
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
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado']
    rtSeleccionado = RecursoTecnologico.objects.get(numeroRT=recursoTecnologicoSeleccionado)
    print(recursoTecnologicoSeleccionado)
    turnosDeRecursoTecnologico = getTurnosDeRecursoTecnologico(rtSeleccionado)

    print(turnosDeRecursoTecnologico)

    context = {
        'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
        'turnosDeRecursoTecnologico': turnosDeRecursoTecnologico,
    }

    return render(request, 'Paso4.html', context)


def getTurnosDeRecursoTecnologico(recursoTecnologicoSeeccionado):
    turnos = recursoTecnologicoSeeccionado.getTurnos()
    turnosParaSeleccion = []
    for turno in turnos:
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
    turnoSeleccionado = request.POST['turnoSeleccionado']

    context = {
        'turnoSeleccionado': turnoSeleccionado,
    }

    return render(request, 'Paso5.html')


def getFechaHoraActual():
    return datetime.now()

def buscarEstadoReservado():
    for estado in Estado.object.all():
        if estado.esAmbitoTurno():
            if estado.getNombre() == "Reservado":
                return estado



