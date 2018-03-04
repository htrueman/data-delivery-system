from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import GitRepoController
from ..constants import ExecutionStatuses


class GitRepoControllerSerializer(serializers.ModelSerializer):
    setup_commands = serializers.CharField(required=False)
    setup_commands_file = serializers.FileField(required=False, source='project_setup_bash_file')

    class Meta:
        model = GitRepoController
        fields = ['id', 'execution_status', 'setup_commands', 'setup_commands_file']
