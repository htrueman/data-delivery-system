import signal
import subprocess
import os
from contextlib import suppress

from django.core.files import File
from django.db import models

from core.models import GitRepository
from .constants import ExecutionStatuses


def get_project_file_path(controller_instance, filename):
    repo_path = controller_instance.repo.local_path
    tools_path = 'tools_{}'.format(os.path.basename(repo_path))
    return os.path.join(tools_path, filename)


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
        upload_to=get_project_file_path,
        null=True)
    project_exec_log_file = models.FileField(
        upload_to=get_project_file_path)
    current_running_process_pid = models.IntegerField(
        null=True,
        blank=True)

    def __str__(self):
        return '{}, {}'.format(self.execution_status, self.repo.deep_link)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__old_execution_status = self.execution_status

    def save(self, *args, **kwargs):
        if not self.project_exec_log_file:
            log_file = open('exec.log', 'w+')
            django_log_file = File(log_file)
            self.project_exec_log_file.save('exec.log', django_log_file)
            log_file.close()
            os.remove('exec.log')
        else:
            super().save(*args, **kwargs)
        if self.execution_status != self.__old_execution_status:
            if self.execution_status == ExecutionStatuses.RUN:
                self.run()
            elif self.execution_status == ExecutionStatuses.STOP:
                self.stop()

    def run(self):
        os.chdir(self.repo.local_path)
        with open(self.project_setup_bash_file.path, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('source {venv_path}/bin/activate\n{body}'.format(
                body=content,
                venv_path=os.path.join(os.path.dirname(self.project_setup_bash_file.path), 'venv')
            ))

        process = subprocess.Popen(['/bin/bash', self.project_setup_bash_file.path],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        self.current_running_process_pid = process.pid
        super().save()

        stdout, stderr = process.communicate()

        with open(self.project_exec_log_file.path, 'a+') as f:
            if stdout:
                f.write(stdout.decode('utf-8'))
            if stderr:
                f.write(stderr.decode('utf-8'))
        self.current_running_process_pid = None
        self.execution_status = ExecutionStatuses.STOP
        super().save()

    def stop(self):
        with suppress(ProcessLookupError):
            os.kill(self.current_running_process_pid, signal.SIGKILL)
        self.current_running_process_pid = None
        super().save()
