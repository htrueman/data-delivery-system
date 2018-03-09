from django.views.generic import DetailView, ListView

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


class GitReposList(ListView):
    template_name = 'local_spider_manager/repos_list.html'
    paginate_by = 10

    def get_queryset(self):
        return GitRepository.objects.filter(user=self.request.user)
