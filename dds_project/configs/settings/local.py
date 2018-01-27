from .base import *

DEBUG = True

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env_variable('PG_NAME'),
        'USER': get_env_variable('PG_USER'),
        'PASSWORD': get_env_variable('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST', '127.0.0.1'),
        'PORT': os.getenv('PG_PORT', '5432')
    }
}
