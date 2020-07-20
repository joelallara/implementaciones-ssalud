from django.urls import path
from .views import ProjectsPageView, ProjectPackagesView, PackageTasksView, BuscadorView, update_projects_info, sql_search

project_patterns = ([
    path('', ProjectsPageView.as_view(), name="list"),
    path('SQL/', BuscadorView.as_view(), name="sql"),
    path('<int:project_pk>/paquetes',
         ProjectPackagesView.as_view(),
         name="packages"
         ),
    path('<int:package_pk>/tareas',
         PackageTasksView.as_view(),
         name="tasks"
         ),
    path('actualizar_info_projectos/',
         update_projects_info,
         name="update_projects_info"
         ),
     path('buscar_sql/',
         sql_search,
         name="sql_search"
         ),
], "project")
