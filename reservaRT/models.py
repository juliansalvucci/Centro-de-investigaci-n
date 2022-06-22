from statistics import mode
from django.db import models

class PersonalCientifico(models.Model):
    legajo = models.CharField(max_length=10) 
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    numeroDocumento = models.CharField(max_length=8)
    correoElectronicoPersonal = models.EmailField()
    correoElectronicoInstitucional = models.EmailField()
    telefonoCelular = models.CharField(max_length=10)

class Sesion(models.Model):
    Usuario = models.ForeignKey('Usuario')

class Usuario(models.Model):
    usuario = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True)

class CentroInvestigacion(models.Model):
    nombre = models.CharField(max_length=20)
    fechaAlta = models.DateField()
    fechaBaja = models.DateField()

class RecursoTecnologico(models.Model):
    numeroRT = models.IntegerField(primary_key=True)
    fechaAlta = models.DateField()
    imagenes = models.ImageField()

class Estado(models.Model):
    nombre = models.CharField()
    descripcion = models.CharField()
    ambito = models.CharField()
    esReservable = models.BooleanField()
    esCancelable = models.BooleanField()

class  CambioEstadoRT(models.Model):
    fechaHoraDesde = models.DateTimeField()
    fechaHoraHasta = models.DateTimeField()

class Modelo(models.Model):
    nombre = models.CharField()

class Marca(models.Model):
    nombre = models.CharField()

class TipoRecursoTecnologico(models.Model): # Modelo para los tipos de recursos tecnologicos
    nombre = models.CharField(max_length=50) # Campo para el nombre del tipo de recurso tecnologico
    descripcion = models.CharField(max_length=100) # campo para la descripcion del tipo de recurso tecnologico

    def getNombre(self): # Funcion para obtener el nombre del tipo de recurso tecnologico
        return self.nombre # Retorno el nombre del tipo de recurso tecnologico
