# Generated by Django 2.0.1 on 2018-03-25 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_gitrepository_cloning_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitrepository',
            name='log_chamber',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]