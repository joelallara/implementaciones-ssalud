from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.apps import apps
from django.template.loader import render_to_string
from django.http import JsonResponse

from core.views import email
from .models import ImplementationRequestHeader, ImplementationRequestDetail
from project.models import Project


@method_decorator(login_required, name='dispatch')
class ImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    queryset = ImplementationRequestHeader.objects.all()
    context_object_name = 'requests'
    paginate_by = 10


@method_decorator(staff_member_required, name='dispatch')
class PendingImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/pending_request_list.html'
    queryset = ImplementationRequestHeader.objects.filter(state='PN').order_by('created')
    context_object_name = 'requests'
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class UserImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        """Return the current user requests"""
        return ImplementationRequestHeader.objects.filter(
            created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class ImplementationRequestDetailView(View):
    def get(self, request, header_pk):
        header = get_object_or_404(ImplementationRequestHeader, pk=header_pk)
        details = header.request_details.all()
        data = dict()
        data['details'] = [model_to_dict(detail) for detail in details]
        if not data['details']:
            data['details'] = None
        return JsonResponse(data)

    def post(self, request):
        project_pk = request.POST.get('selectedProjectid', None)
        packages = request.POST.getlist('package', None)
        project_instance = get_object_or_404(Project, pk=project_pk)
        implementation_request_header = ImplementationRequestHeader.objects.create(
            project=project_instance, created_by=request.user)
        for package in packages:
            tasks = request.POST.getlist(package+'task', None)
            tasks_formated = ", ".join(tasks)
            observations = request.POST.get(package+'observations', '-----')
            if package[0:5] == '-----':
                package = package[0:5]
            else:
                package = package[:-1]
            ImplementationRequestDetail.objects.create(
                request_header=implementation_request_header,
                package=package,
                tasks=tasks_formated,
                observations=observations)

        # Email Sending
        subject = 'Solicitud Deploy a Produccion del proyecto ' + \
            implementation_request_header.project.project_name
        message = 'El usuario "{}" ha realizado una solicitud de deploy del proyecto "{}". Para mas detalles ingrese a http://implementacionesbi/implementaciones/pendientes/'.format(
            implementation_request_header.created_by, implementation_request_header.project.project_name)
        staff_users = User.objects.filter(is_staff=True)
        email_to = [staff_user.email for staff_user in staff_users]
        email(request, subject, message, email_to)

        return redirect(reverse_lazy('request:user_request_list'))


def ajax_search(request):
    data_dict = {}
    search_parameter = request.GET.get("q")
    path = request.GET.get("path")

    if search_parameter:
        if '/mis_solicitudes/' in path:
            requests = ImplementationRequestHeader.objects.filter(
                created_by=request.user, project__project_name__icontains=search_parameter)
        else:
            requests = ImplementationRequestHeader.objects.filter(
                project__project_name__icontains=search_parameter)
        data_dict["is_requests"] = True
    else:
        requests = search_parameter
        data_dict["is_requests"] = False

    if request.is_ajax():
        html = render_to_string(
            template_name="request/request_search_results.html",
            context={"requests": requests}
        )

        data_dict["html_from_view"] = html
        return JsonResponse(data=data_dict, safe=False)
