from django.urls import path
from .views import ImplementationRequestHeaderListView

request_patterns = ([
    path('', ImplementationRequestHeaderListView.as_view(), name='list'),
], 'request')
