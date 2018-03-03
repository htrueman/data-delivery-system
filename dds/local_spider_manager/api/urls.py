from django.urls import path

from . import views

app_name = 'local_spider_manager'

urlpatterns = [
    path('controller/', views.GitRepoControllerAPIView.as_view(), name='controller'),
]
