from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin

from ..models import GitRepoController
from .serializers import GitRepoControllerSerializer


class GitRepoControllerAPIView(GenericAPIView, UpdateModelMixin):
    serializer_class = GitRepoControllerSerializer

    def get_object(self):
        return GitRepoController.objects.get(id=self.request.data['id'])

    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
