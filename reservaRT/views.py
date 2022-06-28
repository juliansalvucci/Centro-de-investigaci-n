import datetime
from django.shortcuts import render
from reservaRT.models import RecursoTecnologico, Sesion, TipoRecursoTecnologico


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

def tomarSeleccionTipoRecursoTecnologico(request):
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']

    context = {
        'tipoRecursoTecnologicoSeleccionado': tipoRecursoTecnologicoSeleccionado,
    }

    return render(request, 'Paso2.html', context)

def getRecursos(request):
    tipoRecursoTecnologicoSeleccionado = request.POST['tipoRecursoTecnologicoSeleccionado']
    tipoRT = TipoRecursoTecnologico.objects.get(nombre = tipoRecursoTecnologicoSeleccionado)

    recursosTecnologicos = obtenerRecursosTecnologico(tipoRT)

    print(recursosTecnologicos)

    context = {
        'recursosTecnologicos': recursosTecnologicos
    }

    return render(request, 'Paso3.html', context)


def obtenerRecursosTecnologico(tipoRT): 
    recursosTecnologicos = []
    for recursoTecnologico in RecursoTecnologico.objects.all():
        if recursoTecnologico.esTuTipoRt(tipoRT):
            if recursoTecnologico.esReservable():
                rt = {
                   'numeroInventario': recursoTecnologico.getNumeroInventario(),
                   'modelo' : recursoTecnologico.getModelo(),
                   'marca': recursoTecnologico.getMarca(),
                   'centroInvestigacion': recursoTecnologico.getCentroInvestigacion(),
                }
                

    return recursosTecnologicos.append(rt)

def ordenarPorCI(request):
    recursosTecnologicosParaMostrar = request.POST['rt']

    recursosTecnologicosParaMostrar.sort(key=lambda x: x['centroInvestigacion'])


def buscarCientificoLoguead(sesion):
    activaSesion = Sesion.objects.get(pk=sesion)
    cientificoLoqueado = activaSesion.getCientifico()
    return cientificoLoqueado

def validarCientifico(request):
    cientificoLogueado = request.POST['cientificoLogueado']

def tomarSeleccionRecursoTecnologico(request):
    recursoTecnologicoSeleccionado = request.POST['recursoTecnologicoSeleccionado']

    context = {
        'recursoTecnologicoSeleccionado': recursoTecnologicoSeleccionado,
    }


def getTurnosDeRecursoTecnologico(recursoTecnologicoSeeccionado):
    turnos = recursoTecnologicoSeeccionado.getTurnos()
    turnosParaSeleccion = []
    for turno in turnos:
        turno.getEstado()
       
    return turnosParaSeleccion.append(turno)
    


def getFechaHoraActual():
    return datetime.now()