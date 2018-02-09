from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.ObtainGitRepoCredentials.as_view(), name='get_git_repo'),
    path('', views.LightSignUp.as_view(), name='light_signup'),
]
