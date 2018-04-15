import subprocess
import re

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field, Button


def get_installed_python_versions():
    process = subprocess.Popen('ls -ls /usr/bin/python*', stdout=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    stdout_lines = [line for line in stdout.decode('utf-8').split('\n')]
    python_versions = []
    for line in stdout_lines:
        if len(line) > 0:
            python_version_line = re.split('(\s)(\d{2}[:]\d{2}|\d{4})(\s)', line)[-1].strip()
            python_key = re.findall('(/[/A-z0-9\.\-]+(\s->)?)', python_version_line)
            if len(python_key) > 0:
                python_path = max(python_key[0]).split(' ->')[0]
                python_versions.append((python_path, python_version_line,))
    return python_versions


class GitRepoManagerForm(forms.Form):
    setup_commands = forms.CharField(required=False, widget=forms.Textarea)
    setup_commands_file = forms.FileField(required=False)
    python_version = forms.ChoiceField(choices=get_installed_python_versions)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'ctrl-form'
        self.helper.form_class = 'col-md-8'
        self.helper.disable_csrf = True

        self.fields['setup_commands'].label = \
            'Write down bash commands for current project execution'
        self.fields['setup_commands_file'].label = \
            'Load bash file with commands for current project execution'

        self.helper.layout = Layout(
            HTML("""
                <div class="setup-note">
                    <p>
                        DO NOT INCLUDE EITHER SETUP OR ACTIVATE VIRTUAL ENVIRONMENT
                        COMMANDS INTO THE BASH COMMANDS INPUTS.
                    </p>
                    <p>
                        JUST CHOOSE YOUR PYTHON VERSION FROM THE LIST OR WRITE DOWN
                        THE FULL PATH TO PYTHON IF DESIRED VERSION IS NOT LISTED.
                    </p>
                </div> 
            """),
            Field('python_version', id='python-version-select'),
            Field('setup_commands', id='setup-commands-textarea'),
            HTML("""
                <div class="ctrl-form-divider">
                    OR
                </div>
            """),
            Field('setup_commands_file', id='setup-commands-file', css_class='form-control'),
            Div(
                Button(
                    css_class='bg-success ctrl-btn', id='run-spider', value='Run', name='run'),
                Button(
                    css_class='bg-danger ctrl-btn', id='stop-spider', value='Stop', name='stop'),
                css_class='ctrl-btns')
        )
