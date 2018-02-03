from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import GitRepository

user = get_user_model()


class ObtainGitRepoCredentialsForm(ModelForm):
    class Meta:
        model = GitRepository
        fields = ['username', 'password', 'deep_link']

    # def save(self, commit=True):
    #     # new_user = user.objects.create(
    #     #     username=self.cleaned_data['username'],
    #     #     password=self.cleaned_data['password']
    #     # )
    #     new_repo = GitRepository.objects.create(**self.cleaned_data)
    #     return new_repo
