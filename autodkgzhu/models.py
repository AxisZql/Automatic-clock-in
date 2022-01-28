from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=64,verbose_name='学号，工号')
    password = models.CharField(max_length=512,verbose_name='密码')
    email = models.CharField(max_length=32,verbose_name='邮箱',null=True)
