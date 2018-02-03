from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ObtainGitRepoCredentialsForm


class ObtainGitRepoCredentials(CreateView):
    form_class = ObtainGitRepoCredentialsForm
    template_name = 'obtain_git_repo_form.html'
    # success_url = reverse_lazy('core:controller')

    # def form_valid(self, form):
    #     new_repo = form.save()
    #     return super().form_valid(form)
