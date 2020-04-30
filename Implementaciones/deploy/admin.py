from django.contrib import admin
from .models import DeployInfo


class DeployInfoAdmin(admin.ModelAdmin):
    list_display = ('deploy_date', 'deploy_by', 'request_header',
                    'lsn')

admin.site.register(DeployInfo,DeployInfoAdmin)
