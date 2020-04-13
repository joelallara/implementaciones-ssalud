from django.contrib import admin
from .models import Project, Package


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'created', 'modified', 'actived', 'reason', 'disabled_date')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'created', 'modified', 'actived', 'reason', 'disabled_date')
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Package, PackageAdmin)