import os
from contextlib import suppress
from django.core.files.base import ContentFile
from rest_framework import serializers

from ..models import GitRepoController


class GitRepoControllerSerializer(serializers.ModelSerializer):
    setup_commands = serializers.CharField(required=False)
    setup_commands_file = serializers.FileField(required=False, source='project_setup_bash_file')

    class Meta:
        model = GitRepoController
        fields = ['id', 'execution_status', 'setup_commands', 'setup_commands_file']

    def update(self, instance, validated_data):
        if 'setup_commands' in validated_data.keys()\
                or 'project_setup_bash_file' in validated_data.keys():
            instance.project_setup_bash_file.delete()
        if 'setup_commands' in validated_data.keys()\
                and 'project_setup_bash_file' not in validated_data.keys():
            script_file_name = 'startup.sh'
            instance.project_setup_bash_file.save(
                script_file_name, ContentFile(validated_data['setup_commands']))
            instance.save()

        return super().update(instance, validated_data)
