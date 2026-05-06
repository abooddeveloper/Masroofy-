from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils import timezone
# Create your models here.



class userRegistration(AbstractUser):
    username=models.CharField(max_length=100,null=False,blank= False,unique=True)
    email=models.EmailField(max_length=200,null=False,blank=False)
    is_first_login=models.BooleanField(default=True)
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]

