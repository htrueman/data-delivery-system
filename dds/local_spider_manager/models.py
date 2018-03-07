import subprocess

import os
from django.db import models

from core.models import GitRepository
from django.dispatch import receiver

from .constants import ExecutionStatuses


def get_project_setup_bash_file_path(controller_instance, filename):
    return os.path.join(os.path.join(controller_instance.repo.local_path, '..'), filename)


class GitRepoController(models.Model):
    repo = models.OneToOneField(
        to=GitRepository,
        on_delete=models.CASCADE,
        related_name='controller')
    execution_status = models.CharField(
        choices=ExecutionStatuses.EXECUTION_STATUSES,
        default=ExecutionStatuses.INITIAL,
        max_length=1)
    project_setup_bash_file = models.FileField(
        upload_to=get_project_setup_bash_file_path,
        null=True)

    def __str__(self):
        return '{}, {}'.format(self.execution_status, self.repo.deep_link)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_execution_status = self.execution_status

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.execution_status != self.__old_execution_status:
            if self.execution_status == ExecutionStatuses.RUN:
                self.run()

    def run(self):
        user_projects_path = os.path.join(self.repo.local_path, '..')
        os.chdir(user_projects_path)

        process = subprocess.Popen(['/bin/bash', self.project_setup_bash_file.path])
        stdout, stderr = process.communicate()

        # venvs_path = os.path.join(os.path.join(local_repo_path, '..'), 'virtualenvs')
        # if not os.path.exists(venvs_path):
        #     os.makedirs(venvs_path)
        # print(stdout, stderr)
        # bash_commands = """
        # cd {venvs_path}
        # virtualenv {venv_name} --no-site-packages
        # source {venv_name}/bin/activate
        # cd {local_path}
        # pip install -r requirements.txt
        # cd mro
        # scrapy list
        # """.format(
        #     venvs_path=venvs_path,
        #     local_path=self.repo.local_path,
        #     venv_name='{}_venv'.format(os.path.basename(local_repo_path)))
