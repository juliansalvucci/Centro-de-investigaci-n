import datetime
from statistics import mode
from django.db import models

#PERSONALCIENCTÍFICO
class PersonalCientifico(models.Model):
    legajo = models.CharField(max_length=10) 
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    numeroDocumento = models.CharField(max_length=8)
    correoElectronicoPersonal = models.EmailField()
    correoElectronicoInstitucional = models.EmailField()
    telefonoCelular = models.CharField(max_length=10)

    def getNombreCompleto(self):
        return self.nombre + " " + self.apellido

#SESIÓN
class Sesion(models.Model):
    usuario = models.ForeignKey('Usuario')

    def getUsuarioEnSesion(self):
        return self.usuario.getCientifico()

#USUARIO
class Usuario(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True)
    personalCientifico = models.ForeignKey('PersonalCientifico')

    def getCientifico(self):
        return self.cientifico.objects.get(self.usuario == self.personalCientifico.getNombreCompleto()) #Suponemos que el nombre de usuario es el nombre completo del científico.

#CENTROINVESTIGACIÓN
class CentroInvestigacion(models.Model):
    nombre = models.CharField(max_length=20)
    fechaAlta = models.DateField()
    fechaBaja = models.DateField()
    recursoTecnologico = models.ManyToManyField('RecursoTecnologico')
    asignacionCientifico = models.ForeignKey('AsignacionCientifico')

    def getRecursosTecnologicos(self):
        recursos = []

        for recurso in self.recursoTecnologico.all():
            recursos.append(recurso)

        return recursos

    def getCientifico(self, cientifico):
        return self.asignacionCientifico.mostrarCientificoDeCi(cientifico)

#ASIGNACIÓNCIENTÍFICO
class AsignacionCientifico(models.Model):
    fechaDesde = models.DateField()
    fechaHasta = models.DateField()
    personalCientifico = models.ForeignKey('PersonalCientifico')

    def mostrarCientificoDeCi(self, cientifico):
        return self.personalCientifico.objects.get(self.personalCientifico.getNombreCompleto() == cientifico)

#RECURSOTECNOLÓGICO
class RecursoTecnologico(models.Model):
    numeroRT = models.IntegerField(primary_key=True)
    fechaAlta = models.DateField()
    fechaBaja = models.DateField()
    imagenes = models.ImageField()
    tipoRecursoTecnologico = models.ForeignKey('TipoRecursoTecnologico')
    turno = models.ManyToManyField('Turno')
    modelo = models.ForeignKey('Modelo')
    #DEPENDENCIA
    centroInvestigacion = models.ForeignKey('CentroInvestigacion')

    def getNumeroInventario(self):
        return self.numeroRT

    def getModelo(self):
        return self.modelo.getNombre()

    def esActivo(self):
        if self.fechaBaja == None:
            return True
        else:
            return False

    def getTurnos(self):
        turnos = []

        for turno in self.turno.all():
            if turno.esDisponible():
                turnos.append(turno)
                
        return turnos

    def getCentroInvestigacion(self):
        return self.centroInvestigacion.getNombre()
    '''
    def esTuTipoRt(self, tipoRT): # Funcion para saber si el recurso tecnologico es de un tipo especifico
        if self.tipoRecursoTecnologico.getNombre() == tipoRT: # Si el tipo de recurso tecnologico es el mismo que el tipoRT
            return True    # Retorno True
        else:              # Si no es el mismo tipo de recurso tecnologico
            return False   # Retorno False

    '''

#ESTADO
class Estado(models.Model):
    nombre = models.CharField()
    descripcion = models.CharField()
    ambito = models.CharField()
    esReservable = models.BooleanField()
    esCancelable = models.BooleanField()

#CAMBIOESTADOTIPORECURSOTECNOLÓGICO
class CambioEstadoRT(models.Model):
    fechaHoraDesde = models.DateTimeField()
    fechaHoraHasta = models.DateTimeField()

#MODELO
class Modelo(models.Model):
    nombre = models.CharField()
    #DEPENDENCIA
    marca = models.ForeignKey('Marca')

    def getNombre(self):
        return self.nombre

    def getMarca(self):
        return self.marca.getNombre()

#MARCA
class Marca(models.Model):
    nombre = models.CharField() 

    def getNombre(self):
        return self.nombre


#TIPORECURSOTECNOLÓGICO
class TipoRecursoTecnologico(models.Model):  # Modelo para los tipos de recursos tecnologicos
    nombre = models.CharField(max_length=50)   # Campo para el nombre del tipo de recurso tecnologico
    descripcion = models.CharField(max_length=100) # campo para la descripcion del tipo de recurso tecnologico
    #DEPENDENCIA
    recursoTecnologico = models.ManyToManyField('RecursoTecnologico') # Campo para los recursos tecnologicos que pertenecen al tipo de recurso tecnologico

    def getNombre(self): # Funcion para obtener el nombre del tipo de recurso tecnologico
        return self.nombre # Retorno el nombre del tipo de recurso tecnologico

    def getRecursosTecnologicosDeTipo(self):
        recursos = []

        for recurso in self.recursoTecnologico.all():

            if(recurso.esActivo()):
                r = {
                    'numeroInventario': recurso.getNumeroInventario(),
                    'modelo': recurso.getModelo(),
                    'marca': recurso.modelo.getMarca(),
                }
                recursos.append(r)

        return recursos

#TURNO
class Turno(models.Model):
    fechaGeneracion = models.DateField()
    diaSemana = models.CharField(max_length=10)
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()

    def esDIsponible(self):
        if self.fechaHoraInicio < datetime.now():
            return True
        else:
            return False

#CAMBIOESTADOTURNO
class CambioEstadoTurno(models.Model):
    fechaHoraDesde = models.DateTimeField()
    fechaHoraHasta = models.DateTimeField()