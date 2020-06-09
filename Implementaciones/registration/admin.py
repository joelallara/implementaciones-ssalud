from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('avatar', 'bio', 'link')


admin.site.register(Profile, ProfileAdmin)
