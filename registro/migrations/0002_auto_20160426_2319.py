# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 02:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comuna',
            name='ciudad',
        ),
        migrations.AlterField(
            model_name='administradoredificio',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Ciudad'),
        ),
        migrations.AlterField(
            model_name='administradoredificio',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Comuna'),
        ),
        migrations.AlterField(
            model_name='condominio',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Ciudad'),
        ),
        migrations.AlterField(
            model_name='condominio',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Comuna'),
        ),
        migrations.AlterField(
            model_name='conserje',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Ciudad'),
        ),
        migrations.AlterField(
            model_name='conserje',
            name='comuna',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoname.Comuna'),
        ),
        migrations.AlterField(
            model_name='departamento',
            name='edificio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edificio', to='registro.Edificio'),
        ),
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.DeleteModel(
            name='Comuna',
        ),
    ]
