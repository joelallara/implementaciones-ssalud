from django.db import models
from datetime import datetime

from core.models import TimeStampedModel, ActivedModel
from BuscadorSSIS.BuscadorSSIS import get_projects_names_from_store


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(actived=True)

    def find_or_create(self, project_name):
        project_list = get_projects_names_from_store()
        for project_name in project_list:
            queryset = self.filter(project_name=project_name)
            if queryset:
                queryset.modified = datetime.now()
            else:
                project = Project.projects.create(project_name=project_name)
        return thread


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

    class Meta:
        verbose_name = "paquete"
        verbose_name_plural = "paquetes"
        ordering = ['-package_name']

    def __str__(self):
        return self.package_name


class Task(TimeStampedModel, ActivedModel):
    task_name = models.CharField(max_length=100, verbose_name="Nombre Tarea")
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='tasks'
        )

    class Meta:
        verbose_name = "tarea"
        verbose_name_plural = "tareas"
        ordering = ['-task_name']

    def __str__(self):
        return self.task_name
