# Generated by Django 2.2.11 on 2020-04-15 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_auto_20200415_1113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='implementationrequestdetail',
            options={'ordering': ['-package'], 'verbose_name': 'solicitud Detalle', 'verbose_name_plural': 'solicitudes Detalles'},
        ),
        migrations.AlterModelOptions(
            name='implementationrequestheader',
            options={'ordering': ['-created'], 'verbose_name': 'solicitud Cabecera', 'verbose_name_plural': 'solicitudes Cabeceras'},
        ),
        migrations.AlterField(
            model_name='implementationrequestheader',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
