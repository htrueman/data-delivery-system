from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import GitRepository

User = get_user_model()


class ObtainGitRepoCredentialsForm(ModelForm):
    class Meta:
        model = GitRepository
        fields = ['username', 'password', 'deep_link']


class LightSignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def validate_email(self):
        user_with_same_email = User.objects.filter(email=self.cleaned_data['email'])
        if user_with_same_email:
            raise ValidationError('User is already registered')
