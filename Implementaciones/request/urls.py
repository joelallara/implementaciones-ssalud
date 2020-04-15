from django.urls import path
from .views import ImplementationRequestHeaderListView, ImplementationRequestDetailView

request_patterns = ([
    path('', ImplementationRequestHeaderListView.as_view(), name='list'),
    path('<int:header_pk>/detalle',
         ImplementationRequestDetailView.as_view(),
         name="detail"
         ),
], 'request')
