from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView, View
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .models import DeployInfo
from request.models import ImplementationRequestHeader
from core.views import email


@method_decorator(login_required, name='dispatch')
class DeployListView(ListView):
    model = DeployInfo
    template_name = 'deploy/deploy_list.html'
    queryset = DeployInfo.objects.all()
    context_object_name = 'deploys'
    paginate_by = 10


@method_decorator(staff_member_required, name='dispatch')
class DeployRequest(View):
    def get(self, request, header_pk):
        header = get_object_or_404(ImplementationRequestHeader, pk=header_pk)
        project_name = header.project.project_name
        created_by = header.created_by.username
        created = timezone.localtime(header.created).strftime(
            '%d/%m/%y %H:%M')  # header.created.strftime("%d/%m/%y")
        data = dict()
        data['header'] = header.id
        data['project_name'] = project_name
        data['created_by'] = created_by
        data['created'] = created
        return JsonResponse(data)

    def post(self, request):
        header_pk = request.POST.get('requestHeader', None)
        lsn = request.POST.get('lsn', None)
        request_header = get_object_or_404(
            ImplementationRequestHeader, pk=header_pk)
        DeployInfo.objects.create(
            deploy_by=request.user, request_header=request_header, lsn=lsn)
        request_header.state = "IM"
        request_header.save()

        # Email Sending
        subject = 'Deploy a Produccion del proyecto ' + \
            request_header.project.project_name
        message = 'Los cambios que ha realizado sobre el proyecto "' + \
            request_header.project.project_name + '" ya se encuentran en producción'
        email_to = request_header.created_by.email
        email(request, subject, message, email_to)
        return redirect(reverse_lazy('deploy:pending') + '?project_name=' + request_header.project.project_name)
