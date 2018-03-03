from rest_framework import serializers

from core.models import GitRepository
from ..constants import ExecutionStatuses


class GitRepoControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitRepository

    def validate_execution_status(self, value):
        if value == ExecutionStatuses.RUN:
            self.run_spider()
        return value

    @staticmethod
    def run_spider():
        pass
