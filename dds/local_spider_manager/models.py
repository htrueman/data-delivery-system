import signal
import subprocess
import os

from django.db import models

from core.models import GitRepository
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
    current_running_process_pid = models.IntegerField(
        null=True,
        blank=True)

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
            elif self.execution_status == ExecutionStatuses.STOP:
                self.stop()

    def run(self):
        user_projects_path = os.path.join(self.repo.local_path, '..')
        os.chdir(user_projects_path)

        process = subprocess.Popen(['/bin/bash', self.project_setup_bash_file.path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        self.current_running_process_pid = process.pid
        super().save()

        stdout, stderr = process.communicate()

        # TODO: use logger here
        with open('log.txt', 'a+') as f:
            f.write(stdout.decode('utf-8'))

    def stop(self):
        os.kill(self.current_running_process_pid, signal.SIGKILL)
        self.current_running_process_pid = None
        super().save()
