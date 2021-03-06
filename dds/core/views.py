from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ObtainGitRepoCredentialsForm, LightSignUpForm
from .models import GitRepository


class ObtainGitRepoCredentials(CreateView):
    form_class = ObtainGitRepoCredentialsForm
    template_name = 'obtain_git_repo_form.html'
    success_url = reverse_lazy('core:light_signup')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            self.request.session['repo_data'] = form.cleaned_data
            return HttpResponseRedirect(self.success_url)
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
        repo_data = self.request.session['repo_data']

        new_user = form.save(commit=False)
        new_user.username = repo_data['username']
        new_user.set_password(repo_data['password'])
        new_user.save()

        GitRepository.objects.create(**repo_data, user=new_user)
        del self.request.session['repo_data']

        return HttpResponseRedirect(self.success_url)
