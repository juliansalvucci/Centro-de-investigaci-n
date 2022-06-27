from django.shortcuts import render
from reservaRT.models import RecursoTecnologico, Sesion, TipoRecursoTecnologico


def mostrarTiposRecursosTecnologicosParaSeleccion(request): # Vista para la opcion de reserva de turno de recurso tecnologico

    tiposRT = buscarTiposRecursosTecnologicos() # Obtengo los tipos de recursos tecnologicos

    context = { # Creo el contexto
        'tiposRT': tiposRT, # Agrego los tipos de recursos tecnologicos
    }

    return render(request, 'index.html', context) # Renderizo la pagina


def buscarTiposRecursosTecnologicos(): # Funcion para buscar los tipos de recursos tecnologicos
    tiposRT = [] # Creo una lista para los tipos de recursos tecnologicos
    for tipos in TipoRecursoTecnologico.objects.all(): # Recorro todos los tipos de recursos tecnologicos
        tiposRT.append(tipos.getNombre()) # Agrego el nombre del tipo de recurso tecnologico a la lista
    
    return tiposRT # Retorno la lista de tipos de recursos tecnologicos



def obtenerRecursoTecnologico(request): 
    recursosTecnologicos = []
    for recursoTecnologico in RecursoTecnologico.objects.all():
        if recursoTecnologico.esTuTipoRt(request.POST['tipoRT']):
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
