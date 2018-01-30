from django.forms import ModelForm

from dds_project.dds.core.models import GitRepository


class ObtainGitRepoCredentialsForm(ModelForm):
    class Meta:
        model = GitRepository
        fields = ['username', 'password', 'deep_link']
