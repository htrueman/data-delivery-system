import os
from git import Repo, GitCommandError
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from django.conf import settings


async def do_git_clone(username, url):
    redis_publisher = RedisPublisher(facility='check-git-clone-status', broadcast=True)

    try:
        Repo.clone_from(
            url,
            os.path.join(settings.CLONED_GIT_REPOS_ROOT, username),
            branch='master'
        )
        status_message = RedisMessage('Your repo is cloned now.')
    except GitCommandError as e:
        status_message = RedisMessage('Your repo is NOT cloned, error: {}'.format(str(e)))
    redis_publisher.publish_message(status_message)
