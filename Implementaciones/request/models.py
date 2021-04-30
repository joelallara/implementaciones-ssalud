from django.db import models

from core.models import TimeStampedModel
from project.models import Project
from django.contrib.auth.models import User


class ImplementationRequestHeader(TimeStampedModel):
    IMPLEMENTED = 'IM'
    PENDING = 'PN'
    STATES = [
        (IMPLEMENTED, 'Implementado'),
        (PENDING, 'Pendiente'),
    ]
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="implementation_requests",
        blank=False)
    state = models.CharField(
        max_length=2,
        choices=STATES,
        default=PENDING,
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "solicitud Cabecera"
        verbose_name_plural = "solicitudes Cabeceras"
        ordering = ["-created"]

    def __str__(self):
        return self.project.project_name


class ImplementationRequestDetail(models.Model):
    request_header = models.ForeignKey(
        ImplementationRequestHeader,
        on_delete=models.CASCADE,
        related_name="request_details")
    package = models.CharField(max_length=1000)
    tasks = models.CharField(max_length=1000)
    observations = models.CharField(max_length=500, blank=False)

    class Meta:
        verbose_name = "solicitud Detalle"
        verbose_name_plural = "solicitudes Detalles"
        ordering = ["-package"]

    def __str__(self):
        return self.package
