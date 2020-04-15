from django.contrib import admin
from .models import ImplementationRequestHeader, ImplementationRequestDetail


class ImplementationRequestHeaderAdmin(admin.ModelAdmin):
    list_display = ('project', 'created', 'modified',
                    'created_by')


class ImplementationRequestDetailAdmin(admin.ModelAdmin):
    list_display = ('request_header', 'package', 'tasks',
                    'observations')


admin.site.register(ImplementationRequestHeader,
                    ImplementationRequestHeaderAdmin)
admin.site.register(ImplementationRequestDetail,
                    ImplementationRequestDetailAdmin)
