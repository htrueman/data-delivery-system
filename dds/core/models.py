import asyncio
from threading import Thread

import os
from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.dispatch import receiver

from .constants import CloningStatuses
from .helpers import get_local_path, do_git_clone


class SystemUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a user with the given username, email and password.
        """
        if not email:
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = SystemUserManager()

    @property
    def is_staff(self):
        return self.is_superuser


class GitRepository(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    deep_link = models.CharField(max_length=150)
    user = models.ForeignKey('SystemUser', on_delete=models.CASCADE)
    local_path = models.CharField(max_length=4096, null=True, blank=True)
    cloning_status = models.IntegerField(
        choices=CloningStatuses.CLONING_STATUSES,
        default=CloningStatuses.PROCESSING)
    log_chamber = models.CharField(max_length=1024, null=True)

    _password = None

    class Meta:
        verbose_name_plural = 'Git repositories'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._password = None

    def save(self, *args, **kwargs):
        self.local_path = get_local_path(self.username, self.deep_link)

        super().save(*args, **kwargs)

        if not os.path.isdir(self.local_path) and self._password is not None:
            self.clone_repo(self._password)

        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def clone_repo(self, raw_password):
        do_git_clone_init = do_git_clone(raw_password, self)

        def start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_until_complete(do_git_clone_init)
            loop.close()

        new_loop = asyncio.new_event_loop()
        thread = Thread(target=start_loop, args=(new_loop,))
        thread.start()

    def __str__(self):
        return '{}'.format(self.deep_link)
