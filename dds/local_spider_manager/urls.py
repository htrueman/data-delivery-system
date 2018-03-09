from django.contrib.auth.decorators import login_required
from django.urls import path, include

from . import views
from .api import urls as api_urls

app_name = 'local_spider_manager'

urlpatterns = [
    path('local/<pk>/', login_required(views.GitRepoInfo.as_view()), name='manager'),
    path('list/', login_required(views.GitReposList.as_view()), name='list'),

    path('api/', include(api_urls, namespace='api'))
]
