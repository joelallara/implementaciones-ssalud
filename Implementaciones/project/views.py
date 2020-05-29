import json
from django.views.generic import ListView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse_lazy

from .buscadorSSIS import get_projects_data
from project.models import Project, Package, Task


class ProjectsPageView(ListView):
    template_name = "project/projects.html"
    queryset = Project.projects.all()
    context_object_name = 'projects'


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
        data = dict()
        data['tasks'] = [model_to_dict(task) for task in tasks]
        if not data['tasks']:
            data['tasks'] = None
        return JsonResponse(data)


def update_projects_info(request):
    try:
        projects_json = get_projects_data()
        projects_dict = json.loads(projects_json)
        for project in projects_dict:
            project_name = project["project_name"]
            print(project_name)
            project_instance, created_project = Project.projects.get_or_create(project_name=project_name)
            print('paso project')
            for package in project["packages"]:
                package_name = package["package_name"]
                print(package_name)
                package_instance, created_package = Package.objects.get_or_create(project=project_instance, package_name=package_name)
                print('paso package')
                for task in package["tasks"]:
                    task_name = task["task_name"]
                    print(task_name)
                    Task.objects.get_or_create(package=package_instance, task_name=task_name)
                    print('paso task')
        return redirect(reverse_lazy('project:list') + '?ok')
    except TypeError as e:
        print(e)
        return redirect(reverse_lazy('project:list') + '?error')
