from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    
        

class Subclient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    client=models.ForeignKey(Client,on_delete=models.SET_NULL,null=True,blank=True)
