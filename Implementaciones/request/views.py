from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import ImplementationRequestHeader, ImplementationRequestDetail
from project.models import Project


class ImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    queryset = ImplementationRequestHeader.objects.all()
    context_object_name = 'requests'
    paginate_by = 10


class PendingImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/pending_request_list.html'
    queryset = ImplementationRequestHeader.objects.filter(state='PN')
    context_object_name = 'requests'
    paginate_by = 10


class UserImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        """Return the current user requests"""
        return ImplementationRequestHeader.objects.filter(
            created_by=self.request.user)


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
            implementation_request_detail = ImplementationRequestDetail.objects.create(
                request_header=implementation_request_header,
                package=package,
                tasks=tasks_formated,
                observations=observations)
        return redirect(reverse_lazy('request:user_request_list'))
        