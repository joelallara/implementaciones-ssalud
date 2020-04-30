from django.urls import path
from .views import DeployListView
from request.views import ImplementationRequestDetailView, PendingImplementationRequestHeaderListView

deploy_patterns = ([
    path('', DeployListView.as_view(), name='list'),
    path('<int:header_pk>/detalle',
         ImplementationRequestDetailView.as_view(),
         name="detail"
         ),
    path('pendientes/',
         PendingImplementationRequestHeaderListView.as_view(),
         name="pending"
         ),
], 'deploy')
