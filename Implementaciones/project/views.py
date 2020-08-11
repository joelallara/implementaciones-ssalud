import json
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse


from .buscadorSSIS import get_projects_data, get_sql_search
from project.models import Project, Package, Task


@method_decorator(login_required, name='dispatch')
class ProjectsPageView(ListView):
    template_name = "project/projects.html"
    queryset = Project.projects.get_queryset_actived
    context_object_name = 'projects'


class GetProjectsJsonList(View):
    def get(self, request):
        projects = Project.projects.get_queryset_actived()
        data = dict()
        data['projects'] = [model_to_dict(project) for project in projects]
        if not data['projects']:
            data['projects'] = None
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class ProjectPackagesView(View):
    def get(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        packages = project.packages.all().filter(actived=True)
        data = dict()
        data['packages'] = [model_to_dict(package) for package in packages]
        if not data['packages']:
            data['packages'] = None
        return JsonResponse(data)


@method_decorator(login_required, name='dispatch')
class PackageTasksView(View):
    def get(self, request, package_pk):
        package = get_object_or_404(Package, pk=package_pk)
        tasks = package.tasks.all().filter(actived=True)
        data = dict()
        data['tasks'] = [model_to_dict(task) for task in tasks]
        if not data['tasks']:
            data['tasks'] = None
        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class BuscadorView(TemplateView):

    template_name = "project/search_sql.html"



def update_projects_info(request):
    try:
        projects_json = get_projects_data()
        projects_dict = json.loads(projects_json)
        for project in projects_dict:
            project_name = project["project_name"]
            project_instance, created_project = Project.projects.all().get_or_create(project_name=project_name)
            for package in project["packages"]:
                package_name = package["package_name"]
                package_instance, created_package = Package.objects.all().get_or_create(project=project_instance, package_name=package_name)
                for task in package["tasks"]:
                    task_name = task["task_name"]
                    Task.objects.all().get_or_create(package=package_instance, task_name=task_name)
        return redirect(reverse_lazy('project:list') + '?ok')
    except TypeError:
        return redirect(reverse_lazy('project:list') + '?error')


def sql_search(request):
    data_dict = {}
    search_parameter = request.GET.get("q")
    check_value = request.GET.get("check_value")

    if search_parameter:
        search = get_sql_search(search_parameter, check_value)
        search_results = search['result']
        data_dict["is_results"] = True
    else:
        search_results = search_parameter
        data_dict["is_results"] = False

    if request.is_ajax():
        html = render_to_string(
            template_name="project/search_sql_results.html",
            context={"search_results": search_results}
        )

        data_dict["html_from_view"] = html
        return JsonResponse(data=data_dict, safe=False)