from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import ImplementationRequestHeader, ImplementationRequestDetail


class ImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    queryset = ImplementationRequestHeader.objects.all()
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
