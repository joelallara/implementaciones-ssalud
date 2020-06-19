from django.urls import path
from .views import DeployListView, DeployRequest, ajax_search_deploy
from request.views import ImplementationRequestDetailView, PendingImplementationRequestHeaderListView

deploy_patterns = ([
    path('', DeployListView.as_view(), name='list'),
    path('<int:header_pk>/detalle',
         DeployRequest.as_view(),
         name="detail"
         ),
    path('pendientes/',
         PendingImplementationRequestHeaderListView.as_view(),
         name="pending"
         ),
    path('pendientes/implementar/',
         DeployRequest.as_view(),
         name="deploy"
         ),
    path('<int:header_pk>/implementar/',
         DeployRequest.as_view(),
         name="deploy_modal"
         ),
    path('buscar/',
         ajax_search_deploy,
         name="ajax_search_deploy"
         ),
], 'deploy')
