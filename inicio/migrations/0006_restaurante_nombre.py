# Generated by Django 4.2.6 on 2023-11-20 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0005_rename_tipococinaid_restaurante_tipococina'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurante',
            name='Nombre',
            field=models.CharField(default='Restaurante', max_length=50),
        ),
    ]