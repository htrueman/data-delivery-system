from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import GitRepoController
from ..constants import ExecutionStatuses


class GitRepoControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitRepoController
        fields = ['id', 'execution_status']

    # def validate_execution_status(self, value):
    #     if value not in ExecutionStatuses.EXECUTION_STATUSES:
    #         raise ValidationError('Unknown command.')
    #     return value

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    @staticmethod
    def run_spider():
        pass
