from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'user'
