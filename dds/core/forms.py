from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import GitRepository

User = get_user_model()


class ObtainGitRepoCredentialsForm(ModelForm):
    class Meta:
        model = GitRepository
        fields = ['username', 'password', 'deep_link']
        widgets = {
            'password': PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if user.is_authenticated:
            self.helper.form_id = 'add-repo-form'
        else:
            self.helper.form_id = 'new-repo-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))


class LightSignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'light-signup-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))

    def validate_email(self):
        user_with_same_email = User.objects.filter(email=self.cleaned_data['email'])
        if user_with_same_email:
            raise ValidationError('User is already registered')


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'light-signup-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))
