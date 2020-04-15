from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse

from .models import ImplementationRequestHeader


class ImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    queryset = ImplementationRequestHeader.objects.all()
    context_object_name = 'requests'
    paginate_by = 10


class ImplementationRequestDetailView(View):
    def get(self, request, header_pk):
        header = get_object_or_404(ImplementationRequestHeader, pk=header_pk)
        details = header.request_details.all()
        data = dict()
        data['details'] = [model_to_dict(detail) for detail in details]
        return JsonResponse(data)
