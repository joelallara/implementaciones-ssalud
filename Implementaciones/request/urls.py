from django.urls import path
from .views import ImplementationRequestHeaderListView, ImplementationRequestDetailView, UserImplementationRequestHeaderListView, ajax_search
from project.views import GetProjectsJsonList

request_patterns = ([
    path('', ImplementationRequestHeaderListView.as_view(), name='list'),
    path('mis_solicitudes/', UserImplementationRequestHeaderListView.as_view(),
         name='user_request_list'),
    path('mis_solicitudes/listado_projectos/',
         GetProjectsJsonList.as_view(), name='json_project_list'),
    path('mis_solicitudes/nueva_solicitud/',
         ImplementationRequestDetailView.as_view(),
         name="new_implementation_request"
         ),
    path('<int:header_pk>/detalle',
         ImplementationRequestDetailView.as_view(),
         name="detail"
         ),
    path('buscar/',
         ajax_search,
         name="ajax_search"
         ),
], 'request')
