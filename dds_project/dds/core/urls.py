from django.urls import path

from . import views

urlpatterns = [
    path('', views.ObtainGitRepoCredentials.as_view(), name='get_git_repo')
]
