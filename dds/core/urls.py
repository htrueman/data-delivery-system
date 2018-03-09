from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.ObtainGitRepoCredentials.as_view(), name='get_git_repo'),
    path('signup-light/', views.LightSignUp.as_view(), name='light_signup'),
    path('login/',
         auth_views.LoginView.as_view(template_name='core/login.html', form_class=LoginForm),
         name='login'),
    path('logout/', auth_views.logout, {'next_page': 'core:get_git_repo'}, name='logout'),
]
