from django.urls import path, include

from . import views
from .api import urls as api_urls

app_name = 'local_spider_manager'

urlpatterns = [
    path('<pk>/', views.GitRepoInfo.as_view(), name='manager'),

    path('api/', include(api_urls, namespace='api'))
]
