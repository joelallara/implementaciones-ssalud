from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse_lazy

from .buscadorSSIS import get_projects_data
from project.models import Project, Package


class ProjectsPageView(ListView):
    template_name = "project/projects.html"
    queryset = Project.projects.all()
    context_object_name = 'projects'
    paginate_by = 10


class GetProjectsJsonList(View):
    def get(self, request):
        projects = Project.projects.all()
        data = dict()
        data['projects'] = [model_to_dict(project) for project in projects]
        if not data['projects']:
            data['projects'] = None
        return JsonResponse(data)


class ProjectPackagesView(View):
    def get(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        packages = project.packages.all()
        data = dict()
        data['packages'] = [model_to_dict(package) for package in packages]
        if not data['packages']:
            data['packages'] = None
        return JsonResponse(data)


class PackageTasksView(View):
    def get(self, request, package_pk):
        package = get_object_or_404(Package, pk=package_pk)
        tasks = package.tasks.all()
        print(tasks)
        data = dict()
        data['tasks'] = [model_to_dict(task) for task in tasks]
        if not data['tasks']:
            data['tasks'] = None
        return JsonResponse(data)


def update_projects_info(request):
    projects = get_projects_data()
    print(projects)
    return redirect(reverse_lazy('project:list'))