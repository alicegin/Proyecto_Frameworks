# Generated by Django 4.2.6 on 2023-11-20 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0006_restaurante_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurante',
            name='CategoriaL',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inicio.categorial'),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='Descripción',
            field=models.CharField(max_length=280, null=True),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='TipoCocina',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inicio.tipococina'),
        ),
    ]
