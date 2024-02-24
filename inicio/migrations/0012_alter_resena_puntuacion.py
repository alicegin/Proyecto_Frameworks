# Generated by Django 4.2.6 on 2023-12-03 04:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0011_fotousuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resena',
            name='Puntuacion',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]