import asyncio
from threading import Thread

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import GitRepository
from .helpers import do_git_clone

User = get_user_model()


class InitNarrowForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'narrow-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))


class ObtainGitRepoCredentialsForm(InitNarrowForm):
    class Meta:
        model = GitRepository
        fields = ['username', 'password', 'deep_link']
        widgets = {
            'password': PasswordInput()
        }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        url = self.cleaned_data['deep_link']
        do_git_clone_init = do_git_clone(username, password, url)

        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_until_complete(do_git_clone_init)
            loop.close()

        new_loop = asyncio.new_event_loop()
        thread = Thread(target=start_loop, args=(new_loop,))
        thread.start()
        return super().clean()


class LightSignUpForm(InitNarrowForm):
    class Meta:
        model = User
        fields = ['email']

    def validate_email(self):
        user_with_same_email = User.objects.filter(email=self.cleaned_data['email'])
        if user_with_same_email:
            raise ValidationError('User is already registered')


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'narrow-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Submit'))
