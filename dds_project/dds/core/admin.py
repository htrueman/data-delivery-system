from django.contrib import admin

from .models import SystemUser, GitRepository

admin.site.register(SystemUser)
admin.site.register(GitRepository)
