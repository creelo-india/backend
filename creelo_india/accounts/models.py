from django.db import models

# Create your models here.
"""custom user model inherited from AbstractUser"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
# from accounts.utils.choices import UserDepartmentChoices
from django.contrib.auth.models import ( BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken    
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where contact_number is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
       
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given contact number and password.

        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    """
    This custom user model for enhanced func.
    """
    username = None
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    email = models.EmailField(null=True, blank=True,unique=True)
    contact_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255,null=True)
    pin_code = models.CharField(max_length=10,null=True)
    city = models.CharField(max_length=100,null=True)
    country = models.CharField(max_length=100,null=True)
    otp=models.CharField(max_length=22,null=True,blank=True)
    password_resetotp=models.CharField(max_length=22,null=True,blank=True)
    is_active = models.BooleanField(default=True)
   
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    class Meta:
        db_table = "user"
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def tokens(self):
      refresh = RefreshToken.for_user(self)
      return {
        'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def __str__(self):
       return self.email
