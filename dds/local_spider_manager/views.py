from django.views.generic import DetailView, ListView

from core.models import GitRepository
from .models import GitRepoController


class GitRepoInfo(DetailView):
    model = GitRepository
    template_name = 'local_spider_manager/manage_local_spider.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        controller, is_created = \
            GitRepoController.objects.get_or_create(repo=self.object)

        if controller.project_setup_bash_file:
            context_data['controller_bash_content'] = ''
            with open(controller.project_setup_bash_file.path, 'r') as f:
                for index, line in enumerate(f):
                    if index <= 512:
                        context_data['controller_bash_content'] += line
                    else:
                        context_data['controller_bash_content'] += 'Last elements are truncated...'
            context_data['controller_log_content'] = ''

        context_data['controller'] = controller
        return context_data


class GitReposList(ListView):
    template_name = 'local_spider_manager/repos_list.html'
    paginate_by = 10

    def get_queryset(self):
        return GitRepository.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if 'remove-all' in request.GET.keys():
            GitRepository.objects.filter(user=request.user).delete()
        return super().get(request, *args, **kwargs)
