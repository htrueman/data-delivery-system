import subprocess

from django.db import models
from django.conf import settings

from core.models import GitRepository
from .constants import ExecutionStatuses


class GitRepoController(models.Model):
    repo = models.OneToOneField(
        to=GitRepository,
        on_delete=models.CASCADE,
        related_name='controller')
    execution_status = models.CharField(
        choices=ExecutionStatuses.EXECUTION_STATUSES,
        default=ExecutionStatuses.INITIAL,
        max_length=1)

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
        # settings.CLONED_GIT_REPOS_ROOT
        bash_commands = """

        """
