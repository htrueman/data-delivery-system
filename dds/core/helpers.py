import os
import re

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


async def do_git_clone(username, password, url):
    redis_publisher = RedisPublisher(facility='check-git-clone-status', broadcast=True)

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
        status_message = RedisMessage('Your repo is cloned now.')
    except Exception as e:
        status_message = RedisMessage('Your repo is NOT cloned, error: {}'.format(str(e)))
    redis_publisher.publish_message(status_message)
