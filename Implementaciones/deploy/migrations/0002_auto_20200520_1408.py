# Generated by Django 2.1.15 on 2020-05-20 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deployinfo',
            options={'ordering': ['-deploy_date'], 'verbose_name': 'implementación Detalle', 'verbose_name_plural': 'implementaciones Detalles'},
        ),
        migrations.AlterField(
            model_name='deployinfo',
            name='deploy_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Implementación'),
        ),
    ]