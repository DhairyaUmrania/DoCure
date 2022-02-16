from asyncio.windows_events import NULL
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.forms import NullBooleanField



# Create your models here.

class User(AbstractUser):
    age=models.IntegerField(null=False, default=0)
    gender=models.CharField(choices=[('Male','Male'),('Female','Female')],max_length=15)
    height=models.IntegerField(null=False, default=0)
    weight=models.IntegerField(null=False, default=0)
    class Meta:  
        db_table = "User"  
       
# class Person(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     address = models.TextField()

class Cbc(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rbc = models.FloatField(null=True,blank=True)
    wbc = models.FloatField( null=True,blank=True   )
    pc = models.FloatField(null=True,blank=True)
    hgb = models.FloatField(null=True,blank=True)
    rcd= models.FloatField(null=True,blank=True)
    mchc = models.FloatField(null=True,blank=True)
    mpv = models.FloatField(null=True,blank=True)
    pcv = models.FloatField(null=True,blank=True,default=NULL)
    mcv = models.FloatField(null=True,blank=True)
    

