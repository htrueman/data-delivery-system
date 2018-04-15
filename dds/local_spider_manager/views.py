from django.views.generic import DetailView, ListView, FormView

from core.models import GitRepository
from .models import GitRepoController
from .forms import GitRepoManagerForm


class GitRepoInfo(DetailView, FormView):
    model = GitRepository
    template_name = 'local_spider_manager/manage_local_spider.html'
    form_class = GitRepoManagerForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        controller, is_created = \
            GitRepoController.objects.get_or_create(repo=self.object)

        if controller.project_setup_bash_file:
            def get_file_content(file_path):
                file_content = ''
                with open(file_path, 'r') as f:
                    for index, line in enumerate(f):
                        if index <= 512:
                            file_content += line
                        else:
                            file_content += 'Last elements are truncated...'
                return file_content

            context_data['controller_bash_content'] = \
                get_file_content(controller.project_setup_bash_file.path)
            context_data['controller_log_content'] = \
                get_file_content(controller.project_exec_log_file.path)

        context_data['controller'] = controller
        return context_data


class GitReposList(ListView):
    template_name = 'local_spider_manager/repos_list.html'
    paginate_by = 10

    def get_queryset(self):
        return GitRepository.objects.filter(user=self.request.user).order_by('-id')

    def get(self, request, *args, **kwargs):
        if 'remove-all' in request.GET.keys():
            GitRepository.objects.filter(user=request.user).delete()
        return super().get(request, *args, **kwargs)
