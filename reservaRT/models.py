from statistics import mode
from django.db import models

#PERSONALCIENCTÍFICO
class PersonalCientifico(models.Model):
    legajo = models.CharField(max_length=10, blank=True, null=True) 
    nombre = models.CharField(max_length=20 , blank=True, null=True)
    apellido = models.CharField(max_length=20 , blank=True, null=True)
    numeroDocumento = models.CharField(max_length=8,blank=True, null=True)
    correoElectronicoPersonal = models.EmailField(blank=True, null=True)
    correoElectronicoInstitucional = models.EmailField(blank=True, null=True)
    telefonoCelular = models.CharField(max_length=10,blank=True, null=True)

    def getLegajo(self):
        return self.legajo

#SESIÓN
class Sesion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)

    def getUsuarioEnSesion(self):
        return self.usuario.getCientifico()

#USUARIO
class Usuario(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True)
    PunteroPersonalCientifico = models.ForeignKey("PersonalCientifico", on_delete=models.CASCADE, blank=True ,null=True)

    def getCientifico(self):
        return self.PunteroPersonalCientifico.getLegajo()

#CENTROINVESTIGACIÓN
class CentroInvestigacion(models.Model):
    nombre = models.CharField(max_length=20)
    fechaAlta = models.DateField()
    fechaBaja = models.DateField(blank=True, null=True)
    recursoTecnologico = models.ManyToManyField('RecursoTecnologico')
    asignacionCientifico = models.ForeignKey('AsignacionCientificoDelCI', on_delete=models.CASCADE, blank=True, null=True)

    def getNombre(self):
        return self.nombre

    def misRecursosTecnologicos(self):
        recursos = []

        for recurso in self.recursoTecnologico.all():
            recursos.append(recurso)

        return recursos

    #En diagrama es validar cientifico, luego cambiar en diagrama.
    def getCientifico(self, cientifico):
        return self.asignacionCientifico.mostrarCientificoDeCi(cientifico)

#ASIGNACIÓNCIENTÍFICO
class AsignacionCientificoDelCI(models.Model):
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(blank=True, null=True)
    personalCientifico = models.ManyToManyField("PersonalCientifico")

    def mostrarCientificoDeCi(self, cientifico):
        if self.personalCientifico.filter(legajo=cientifico):
            return True
        else:
            return False
        
       

#RECURSOTECNOLÓGICO
class RecursoTecnologico(models.Model):
    numeroRT = models.IntegerField(primary_key=True)
    fechaAlta = models.DateField()
    fechaBaja = models.DateField(blank=True, null=True)
    imagenes = models.ImageField(blank=True, null=True)
    tipoRecursoTecnologico = models.ForeignKey("TipoRecursoTecnologico", on_delete=models.CASCADE, blank=True, null=True)
    turno = models.ManyToManyField('Turno', blank=True, null=True)
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE, blank=True, null=True)
    cambioEstadoRecursoTecnologico = models.ForeignKey('CambioEstadoRT', on_delete=models.CASCADE, blank=True, null=True)
    #DEPENDENCIA
    centroInvestigacion = models.ForeignKey("CentroInvestigacion", on_delete=models.CASCADE, blank=True, null=True)

    def getNumeroInventario(self):
        return self.numeroRT

    def getModelo(self):
        return self.modelo.getNombre()

    def getMarca(self):
        return self.modelo.getMarca()

    def esReservable(self):
        return True
        #return self.cambioEstadoRecursoTecnologico.esReservable()

    def validarCientifico(self, cientifico):
        return self.centroInvestigacion.getCientifico(cientifico)

    def getTurnos(self):
        turnos = []
        for turno in self.turno.all():
            turnos.append(turno)
                
        return turnos

    def getCentroInvestigacion(self):
        return self.centroInvestigacion.getNombre()
    
    def esTuTipoRt(self, tipoRT): # Funcion para saber si el recurso tecnologico es de un tipo especifico
        print(self.tipoRecursoTecnologico.getNombre())
        if self.tipoRecursoTecnologico.getNombre() == tipoRT: # Si el tipo de recurso tecnologico es el mismo que el tipoRT
            return True    # Retorno True
        else:              # Si no es el mismo tipo de recurso tecnologico
            return False   # Retorno False

    

#ESTADO
class Estado(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    ambito = models.CharField(max_length=20)
    esReservable = models.BooleanField()
    esCancelable = models.BooleanField()

    def esAmbitoTurno(self):
        if self.ambito == "Turno":
           return True

    def getNombre(self):
        return self.nombre

    def esReservable(self):
        return self.esReservable == True

#CAMBIOESTADOTIPORECURSOTECNOLÓGICO
class CambioEstadoRT(models.Model):
    fechaHoraDesde = models.DateTimeField()
    fechaHoraHasta = models.DateTimeField()

    def esReservable(self):
        return self.estado.getEsReservable()

   

#MODELO
class Modelo(models.Model):
    nombre = models.CharField(max_length=20)
    #DEPENDENCIA
    marca = models.ForeignKey('Marca', on_delete=models.CASCADE)

    def getNombre(self):
        return self.nombre

    def getMarca(self):
        return self.marca.getNombre()

#MARCA
class Marca(models.Model):
    nombre = models.CharField(max_length=10) 

    def getNombre(self):
        return self.nombre


#TIPORECURSOTECNOLÓGICO
class TipoRecursoTecnologico(models.Model):  # Modelo para los tipos de recursos tecnologicos
    nombre = models.CharField(max_length=50)   # Campo para el nombre del tipo de recurso tecnologico
    descripcion = models.CharField(max_length=100) # campo para la descripcion del tipo de recurso tecnologico
    #DEPENDENCIA
    recursoTecnologico = models.ManyToManyField('RecursoTecnologico', blank=True, null=True) # Campo para los recursos tecnologicos que pertenecen al tipo de recurso tecnologico

    def getNombre(self): # Funcion para obtener el nombre del tipo de recurso tecnologico
        return self.nombre # Retorno el nombre del tipo de recurso tecnologico


#TURNO
class Turno(models.Model):
    fechaGeneracion = models.DateField()
    diaSemana = models.CharField(max_length=10)
    fechaHoraInicio = models.DateTimeField()
    fechaHoraFin = models.DateTimeField()
    cambioEstadoTurno = models.ForeignKey('CambioEstadoTurno', on_delete=models.CASCADE, blank=True, null=True)

    def getFechaGeneracion(self):
        return self.fechaGeneracion

    def getDiaSemana(self):
        return self.diaSemana

    def getFechaHoraInicio(self):
        return self.fechaHoraInicio

    def getFechaHoraFin(self):
        return self.fechaHoraFin

    def getEstado(self):
        return self.cambioEstadoTurno.getEstado()

    def crearNuevoCambioEstadoTurno(self,fechaHoraDesde,fechaHoraHasta, estado):
        cambioEstadoTurno = CambioEstadoTurno.objects.create()
        cambioEstadoTurno.new(fechaHoraDesde, fechaHoraHasta, estado)
        cambioEstadoTurno.save()
        self.cambioEstadoTurno.add(cambioEstadoTurno)
        self.save()


#CAMBIOESTADOTURNO
class CambioEstadoTurno(models.Model):
    fechaHoraDesde = models.DateTimeField()
    fechaHoraHasta = models.DateTimeField(blank=True, null=True)
    estado = models.ForeignKey("Estado", on_delete=models.CASCADE)

    def getEstado(self):
        return self.estado.getNombre()
    
    def esReservable(self):
        return self.estado.esReservable()

    def setEstado(self, estado):
        self.estado = estado

    def new(self, fechaHoraDesde, fechaHoraHasta, estado):
        self.fechaHoraDesde = fechaHoraDesde
        self.fechaHoraHasta = fechaHoraHasta
        self.setEstado(estado)