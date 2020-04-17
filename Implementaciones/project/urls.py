from django.urls import path
from .views import ProjectsPageView, ProjectPackagesView, PackageTasksView

project_patterns = ([
    path('', ProjectsPageView.as_view(), name="list"),
    path('<int:project_pk>/paquetes',
         ProjectPackagesView.as_view(),
         name="packages"
         ),
    path('<int:package_pk>/tareas',
         PackageTasksView.as_view(),
         name="tasks"
         ),
], "project")
