from django.db import models

from project.models import Project


class ImplementationRequestHeader(models.Model):
    IMPLEMENTED = 'IM'
    PENDING = 'PN'
    STATES = [
        (IMPLEMENTED, 'Implementado'),
        (PENDING, 'Pendiente'),
    ]
    request_date = models.DateTimeField(auto_now=True)
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

    class Meta:
        ordering = ["-request_date"]

    def __str__(self):
        return self.project.project_name


class ImplementationRequestDetail(models.Model):
    request_header = models.ForeignKey(
        ImplementationRequestHeader,
        on_delete=models.CASCADE,
        related_name="request_details")
    package = models.CharField(max_length=80)
    tasks = models.CharField(max_length=200)
    observations = models.CharField(max_length=500, blank=False)

    class Meta:
        ordering = ["-package"]

    def __str__(self):
        return self.package
