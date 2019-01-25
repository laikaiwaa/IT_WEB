from django.db import models

class userinfo(models.Model):
    userid=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=30, unique=True,null=False)
    password=models.CharField(max_length=30)
    type=models.CharField(max_length=5)
class loginhistory(models.Model):
    userid=models.IntegerField()
    username=models.CharField(max_length=30)
    time=models.DateTimeField(auto_now=True)

