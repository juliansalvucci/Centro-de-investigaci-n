from django.db import models
from django.forms import CharField

class Usuario(models.Model):
    nombreUsuario = CharField(max_length=10)


