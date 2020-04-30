from django.db import models
from django.contrib.auth.models import User

from request.models import ImplementationRequestHeader



class DeployInfo(models.Model):
    deploy_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha Implementación",
        null=True
        )
    deploy_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    request_header = models.ForeignKey(
        ImplementationRequestHeader,
        on_delete=models.CASCADE,
        related_name="deploy_info")
    lsn = models.PositiveIntegerField()
    

    class Meta:
        verbose_name = "implementación Detalle"
        verbose_name_plural = "implementaciones Detalles"
        ordering = ["-deploy_date"]

    def __str__(self):
        return '{}'.format(self.deploy_date)
