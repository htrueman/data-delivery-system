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

        venv_name = 'venv'
        if instance.project_setup_bash_file \
                and not os.path.exists(os.path.join(
                    os.path.dirname(instance.project_setup_bash_file.path), venv_name)):
            os.chdir(os.path.dirname(instance.project_setup_bash_file.path))
            process = subprocess.Popen(
                ['virtualenv',
                 '--python',
                 validated_data['python_version'],
                 venv_name,
                 '--no-site-packages'],
                stdout=subprocess.PIPE)
            stdout, stderr = process.communicate()
            with open(instance.project_exec_log_file.path, 'a+') as f:
                if stdout:
                    f.write(stdout.decode('utf-8'))
                if stderr:
                    f.write(stderr.decode('utf-8'))

        return super().update(instance, validated_data)
