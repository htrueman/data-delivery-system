from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from core.models import GitRepository
from .serializers import GitRepoControllerSerializer


class GitRepoControllerAPIView(GenericAPIView, UpdateModelMixin):
    model = GitRepository
    serializer_class = GitRepoControllerSerializer

    def post(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
