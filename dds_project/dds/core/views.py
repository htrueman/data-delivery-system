from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ObtainGitRepoCredentialsForm, LightSignUpForm


class ObtainGitRepoCredentials(CreateView):
    form_class = ObtainGitRepoCredentialsForm
    template_name = 'obtain_git_repo_form.html'
    success_url = reverse_lazy('core:light_signup')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            self.request.session['repo'] = form.save(commit=False)
            return HttpResponseRedirect(self.get_success_url())
        else:
            extra_repo = form.save(commit=False)
            extra_repo.user = self.request.user
            extra_repo.save()
            return HttpResponseRedirect('some_path')


class LightSignUp(CreateView):
    form_class = LightSignUpForm
    template_name = 'registration/light_sign_up_form.html'
    success_url = reverse_lazy('some_path')

    def form_valid(self, form):
        repo = self.request.session['repo']
        new_user = form.save(commit=False)
        new_user.username = repo.username
        new_user.password = repo.password
        new_user.save()

        repo.user = new_user
        repo.save()
        return HttpResponseRedirect(self.get_success_url())
