# Generated by Django 4.0.4 on 2022-07-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservaRT', '0016_alter_estado_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cambioestadort',
            name='fechaHoraHasta',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
