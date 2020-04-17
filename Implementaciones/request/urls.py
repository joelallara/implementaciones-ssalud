from django.urls import path
from .views import ImplementationRequestHeaderListView, ImplementationRequestDetailView, UserImplementationRequestHeaderListView
from project.views import GetProjectsJsonList

request_patterns = ([
    path('', ImplementationRequestHeaderListView.as_view(), name='list'),
    path('mis_solicitudes/', UserImplementationRequestHeaderListView.as_view(),
         name='user_request_list'),
    path('mis_solicitudes/listado_projectos/',
         GetProjectsJsonList.as_view(), name='json_project_list'),
    path('<int:header_pk>/detalle',
         ImplementationRequestDetailView.as_view(),
         name="detail"
         ),
], 'request')
