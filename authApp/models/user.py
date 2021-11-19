from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, identify, password=None):
        if not identify:
            raise ValueError('Los usuarios deben tener un nombre')
        user = self.model(username=identify)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identify, password):
        user = self.create_user(
            identify=identify,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    identify = models.IntegerField('Identify', unique=True)
    password = models.CharField('Password', max_length=256)
    name = models.CharField('Name', max_length=30)
    phone = models.IntegerField('Phone')
    address = models.CharField('Address', max_length=100)
    city = models.CharField('City', max_length=30)
    is_admin = models.BooleanField('Admin')

    def save(self, **kwargs):
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN'
        self.password = make_password(self.password,  some_salt)
        super().save(**kwargs)

    objects = UserManager()
    USERNAME_FIELD = 'identify'
