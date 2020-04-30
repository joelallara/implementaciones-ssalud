from django.shortcuts import render
from django.views.generic.list import ListView

from .models import DeployInfo


class DeployListView(ListView):
    model = DeployInfo
    template_name = 'deploy/deploy_list.html'
    queryset = DeployInfo.objects.all()
    context_object_name = 'deploys'
    paginate_by = 10
