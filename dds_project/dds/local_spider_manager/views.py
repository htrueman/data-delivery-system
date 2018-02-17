import json

from django.views.generic import DetailView
from dds.core.models import GitRepository


class GitRepoController(DetailView):
    model = GitRepository
    template_name = 'manage_local_spider.html'

    def post(self, request, *args, **kwargs):
        run_spider = json.loads(request.POST.get('run_spider'))
        if run_spider:
            pass
