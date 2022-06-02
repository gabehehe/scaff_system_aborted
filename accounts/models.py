#https://www.codingforentrepreneurs.com/blog/how-to-create-a-custom-django-user-model
#https://www.youtube.com/watch?v=HshbjK1vDtY
from django.db import models
from . import enums

from django.contrib.auth.models import (
    AbstractBaseUser,BaseUserManager
)

class TypeUser(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False)
    objects = models.Manager()

    def __str__(self):
        return self.description


class UserManager(BaseUserManager):
    def create_user(self, username, type_user=enums.TypeUsersEnum.VISITANTE.value, is_staff=False, is_admin=False, is_active=True):
        if not username:
            raise ValueError("Username obrigatório")
        user_obj = self.model(
            username = self.normalize_username(username)
        )
        user_obj.type_user = type_user
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username):
        user = self.create_user(
            username,
            is_staff=True
        )
        return user

    def create_superuser(self, username):
        user = self.create_user(
            username,
            is_staff=True,
            is_admin=True
        )
        return user




#class User(models.Model):
class User(AbstractBaseUser):
    type_user = models.ForeignKey(TypeUser, on_delete=models.CASCADE, default=enums.TypeUsersEnum.VISITANTE.value)
    username = models.CharField(max_length=255, blank=False, null=False, unique=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
   # nick_name = models.CharField(max_length=255, blank=True, null=True)



    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()
    #objects = models.Manager()

    @property
    def is_staff(self):
        return self.staff


    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(selfself, app_label):
        return True