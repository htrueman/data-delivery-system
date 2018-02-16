from django.urls import path

from . import views

app_name = 'local_spider_manager'

urlpatterns = [
    path('<pk>/', views.GitRepoController.as_view(), name='local_spider_manager'),
]
