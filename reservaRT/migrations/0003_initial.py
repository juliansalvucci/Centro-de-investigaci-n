# Generated by Django 4.0.4 on 2022-06-20 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reservaRT', '0002_delete_alumno'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoRecursotecnologico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
    ]