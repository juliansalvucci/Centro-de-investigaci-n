# Generated by Django 4.0.4 on 2022-06-29 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservaRT', '0002_usuario_punteropersonalcientifico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='nombre',
            field=models.CharField(max_length=10),
        ),
    ]
