from django.views.generic import DetailView

from dds.core.models import GitRepository


class GitRepoController(DetailView):
    model = GitRepository
    template_name = 'manage_local_spider.html'
