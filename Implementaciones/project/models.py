from django.db import models
from datetime import datetime

from core.models import TimeStampedModel, ActivedModel


class ProjectManager(models.Manager):
    def get_queryset_actived(self):
        return super(ProjectManager, self).get_queryset().filter(actived=True)


class Project(TimeStampedModel, ActivedModel):
    project_name = models.CharField(
        max_length=100,
        verbose_name="Nombre Proyecto"
        )
    projects = ProjectManager()

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos"
        ordering = ['project_name']

    def __str__(self):
        return self.project_name


class PackageManager(models.Manager):
    def get_queryset_actived(self):
        return super(PackageManager, self).get_queryset().filter(actived=True)


class Package(TimeStampedModel, ActivedModel):
    package_name = models.CharField(
        max_length=100,
        verbose_name="Nombre Paquete"
        )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='packages'
        )
    objects = PackageManager()

    class Meta:
        verbose_name = "paquete"
        verbose_name_plural = "paquetes"
        ordering = ['package_name']

    def __str__(self):
        return self.package_name


class TaskManager(models.Manager):
    def get_queryset_actived(self):
        return super(TaskManager, self).get_queryset().filter(actived=True)


class Task(TimeStampedModel, ActivedModel):
    task_name = models.CharField(max_length=1000, verbose_name="Nombre Tarea")
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='tasks'
        )
    objects = TaskManager()

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"
        ordering = ['task_name']

    def __str__(self):
        return self.task_name
