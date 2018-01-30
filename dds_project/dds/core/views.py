from django.views.generic import FormView

from dds_project.dds.core.forms import ObtainGitRepoCredentialsForm


class ObtainGitRepoCredentials(FormView):
    form_class = ObtainGitRepoCredentialsForm
    template_name = 'obtain_git_repo_form.html'

    def form_valid(self, form):
        pass
