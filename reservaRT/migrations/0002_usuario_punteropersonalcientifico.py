# Generated by Django 4.0.4 on 2022-06-29 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservaRT', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='PunteroPersonalCientifico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservaRT.personalcientifico'),
        ),
    ]