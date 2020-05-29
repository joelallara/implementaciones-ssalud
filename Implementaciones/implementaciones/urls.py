from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.static import serve
from django.conf.urls.static import static

from project.urls import project_patterns
from profiles.urls import profiles_patterns
from request.urls import request_patterns
from deploy.urls import deploy_patterns


# Change the redirect to my login template and not to the admin login when a view has staff_member_required decorator 
admin.site.login = staff_member_required(
    admin.site.login, login_url=settings.LOGIN_URL)

urlpatterns = [
    # Paths core
    path('', include('core.urls')),

    # Paths project
    path('proyectos/', include(project_patterns)),

    # Paths request
    path('solicitudes/', include(request_patterns)),

    # Paths deploy
    path('implementaciones/', include(deploy_patterns)),

    # Paths del admin
    path('admin/', admin.site.urls),

    # Paths de Auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),

    # Paths de Profiles
    path('profiles/', include(profiles_patterns)),
]

urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)