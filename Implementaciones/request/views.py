from django.shortcuts import render
from django.views.generic.list import ListView

from .models import ImplementationRequestHeader


class ImplementationRequestHeaderListView(ListView):
    model = ImplementationRequestHeader
    template_name = 'request/request_list.html'
    queryset = ImplementationRequestHeader.objects.all()
    context_object_name = 'requests'
    paginate_by = 10
