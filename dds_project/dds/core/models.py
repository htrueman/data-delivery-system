from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class SystemUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=50)
    git_repository = models.ForeignKey('GitRepository', null=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'


class GitRepository(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=128)
    deep_link = models.CharField(max_length=150)
