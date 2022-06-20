from django.db import models

class Alumno(models.Model):
    nombreAlumno = models.CharField(max_length=50)

