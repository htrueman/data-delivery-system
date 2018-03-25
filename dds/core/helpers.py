import json
import os
import re

from core.constants import CloningStatuses
from git import Repo
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from django.conf import settings


def get_local_path(username, url):
    pat = re.compile('[\W]+', re.UNICODE)
    repo_dir_name = re.sub(pat, '_', url)
    local_path = os.path.join(
        os.path.join(settings.CLONED_GIT_REPOS_ROOT, username), repo_dir_name)
    return local_path


async def do_git_clone(username, password, url, repo):
    redis_publisher = RedisPublisher(facility='check-git-clone-status', broadcast=True)
    status_message = {
        'id': repo.id
    }
    try:
        url_with_creds = 'https://{username}:{password}@{path}'.format(
            path=url.split('https://')[1],
            username=username,
            password=password)

        Repo.clone_from(
            url_with_creds,
            get_local_path(username, url),
            branch='master'
        )
        repo.cloning_status = CloningStatuses.SUCCEED
        status_message['type'] = 'success'
    except Exception as e:
        repo.cloning_status = CloningStatuses.FAILED
        status_message['type'] = 'fail'
        status_message['error_text'] = str(e)
    repo.save()
    redis_publisher.publish_message(RedisMessage(json.dumps(status_message)))
