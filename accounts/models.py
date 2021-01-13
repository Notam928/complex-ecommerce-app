from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
    )


class UserManager(BaseUserManager):
    
    def create_user(self, email, first_name, password=None, **extra_fields):
        """
        Create user 
        
        :return user
        """
        if not email:
            raise ValueError("User must have an email address")
        
        now = timezone.now()
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        
        user.set_password(password)
        # use default database to save user
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, first_name, password=None):
        
        user = self.create_user(
            email=email, 
            password=password,
            first_name=first_name,
        )
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user
        
    
    
class User(AbstractBaseUser,PermissionsMixin):
    #The user model custom
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='date updated', auto_now=True)
    
    
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name",]
    
    
    def __str__(self):
        """
        Unicode representation for an user model.
        :return: string
        """
        return self.email
    
    def get_full_name(self):
        """
        User fullname (first_name + last_name)
        :return string
        """
        return "{0} {1}".format(self.first_name, self.last_name)
    
    def get_short_name(self):
        """
        Short name of user => first_name
        :return string
        """
        return self.first_name
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
    
    
    
class Post(models.Model):
    pass
    
