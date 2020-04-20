from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.edit import CreateView
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
        project_pk = request.POST.get('projectSelectpicker', None)
        print(project_pk)
        project = get_object_or_404(Project, pk=project_pk)
        #implementation_request_header = ImplementationRequestHeader.create(
         #   project=project.id, created_by=request.user)
        return redirect(reverse_lazy('request:user_request_list'))


    #     def add_message(request, pk):
    # json_response = {'created':False}
    # if request.user.is_authenticated:
    #     content = request.GET.get('content', None)
    #     if content:
    #         thread = get_object_or_404(Thread, pk=pk)
    #         message = Message.objects.create(user=request.user, content=content)
    #         thread.messages.add(message)
    #         json_response['created'] = True
    #         if len(thread.messages.all()) is 1:
    #             json_response['first'] = True
    # else:
    #     raise Http404("User is not authenticated")
    # return JsonResponse(json_response)
