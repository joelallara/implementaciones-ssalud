from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from project.urls import project_patterns
from profiles.urls import profiles_patterns
from request.urls import request_patterns

urlpatterns = [
    # Paths core
    path('', include('core.urls')),

    # Paths project
    path('proyectos/', include(project_patterns)),

    # Paths request
    path('solicitudes/', include(request_patterns)),

    # Paths del admin
    path('admin/', admin.site.urls),

    # Paths de Auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),

    # Paths de Profiles
    path('profiles/', include(profiles_patterns)),
]
