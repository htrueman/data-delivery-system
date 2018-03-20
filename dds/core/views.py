import json

from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ObtainGitRepoCredentialsForm, LightSignUpForm
from .models import GitRepository


class ObtainGitRepoCredentials(CreateView):
    form_class = ObtainGitRepoCredentialsForm
    template_name = 'core/obtain_git_repo_form.html'
    success_url = reverse_lazy('core:light_signup')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            self.request.session['repo_data'] = form.cleaned_data
            self.request.session['is_ajax_submit'] = \
                json.loads(self.request.POST.get('is_ajax_submit'))
            return HttpResponseRedirect(self.success_url)
        else:
            extra_repo = form.save(commit=False)
            extra_repo.user = self.request.user
            extra_repo.save()
            return HttpResponseRedirect(
                reverse_lazy('local_spider_manager:manager', kwargs={'pk': extra_repo.id}))


class LightSignUp(CreateView):
    form_class = LightSignUpForm
    template_name = 'core/light_sign_up_form.html'
    is_ajax_submit_template_name = 'core/light_sign_up_form_body.html'

    def dispatch(self, request, *args, **kwargs):
        self.is_ajax_submit = self.request.session.get('is_ajax_submit')
        if self.is_ajax_submit:
            self.repo_data = self.request.session['repo_data']
            return super().dispatch(request, *args, **kwargs)
        return HttpResponse("Forbidden", status=403)

    def get_success_url(self):
        return reverse_lazy('local_spider_manager:manager', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        if self.is_ajax_submit:
            return render(
                self.request, self.is_ajax_submit_template_name, {'form': self.form_class})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.username = self.repo_data['username']
        new_user.set_password(self.repo_data['password'])
        new_user.save()

        GitRepository.objects.create(**self.repo_data, user=new_user)
        del self.request.session['repo_data']
        del self.request.session['is_ajax_submit']

        login(self.request, new_user)

        return super().form_valid(form)
