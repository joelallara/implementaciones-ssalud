from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView, View
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone

from .models import DeployInfo
from request.models import ImplementationRequestHeader


class DeployListView(ListView):
    model = DeployInfo
    template_name = 'deploy/deploy_list.html'
    queryset = DeployInfo.objects.all()
    context_object_name = 'deploys'
    paginate_by = 10


class DeployRequest(View):
    def get(self, request, header_pk):
        header = get_object_or_404(ImplementationRequestHeader, pk=header_pk)
        project_name = header.project.project_name
        created_by = header.created_by.username
        created = timezone.localtime(header.created).strftime('%d/%m/%y %H:%M') #header.created.strftime("%d/%m/%y")
        data = dict()
        data['header'] = header.id
        data['project_name'] = project_name
        data['created_by'] = created_by
        data['created'] = created
        return JsonResponse(data)

    def post(self, request):
        header_pk = request.POST.get('requestHeader', None)
        lsn = request.POST.get('lsn', None)
        request_header = get_object_or_404(ImplementationRequestHeader, pk=header_pk)
        deploy_info = DeployInfo.objects.create(deploy_by=request.user, request_header=request_header, lsn=lsn)
        request_header.state = "IM"
        request_header.save()
        return redirect(reverse_lazy('deploy:pending'))