# Generated by Django 4.0.4 on 2022-07-04 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservaRT', '0015_cambioestadort_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
