import json
import git

from django.views.generic import DetailView
from dds.core.models import GitRepository


class GitRepoController(DetailView):
    model = GitRepository
    template_name = 'manage_local_spider.html'

    def post(self, request, *args, **kwargs):
        command = json.loads(request.body)
        if command.get('run_spider'):
            pass
