import subprocess
import os

from django.core.files.base import ContentFile

from rest_framework import serializers

from ..models import GitRepoController


class GitRepoControllerSerializer(serializers.ModelSerializer):
    setup_commands = serializers.CharField(required=False)
    setup_commands_file = serializers.FileField(required=False, source='project_setup_bash_file')
    python_version = serializers.CharField()

    class Meta:
        model = GitRepoController
        fields = ['id', 'execution_status', 'setup_commands',
                  'setup_commands_file', 'python_version']

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

        if instance.project_setup_bash_file:
            os.chdir(os.path.dirname(instance.project_setup_bash_file.path))
            subprocess.Popen(
                ['virtualenv',
                 '--python',
                 validated_data['python_version'],
                 'venv',
                 '--no-site-packages'])

        return super().update(instance, validated_data)
