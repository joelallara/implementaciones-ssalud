from django.views.generic.base import TemplateView
from django.shortcuts import render

from project.models import Project


class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get(self, request, *args, **kwargs):
        projects = Project.projects.all()
        return render(request, self.template_name, {'projects': projects})
