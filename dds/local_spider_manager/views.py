from django.views.generic import DetailView

from core.models import GitRepository
from .models import GitRepoController


class GitRepoInfo(DetailView):
    model = GitRepository
    template_name = 'local_spider_manager/manage_local_spider.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['controller'], is_created = \
            GitRepoController.objects.get_or_create(repo=self.object)
        return context_data
