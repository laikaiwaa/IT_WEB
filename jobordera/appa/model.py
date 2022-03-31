from django.db import models


class userinfo(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=30)
    type = models.CharField(max_length=5)

class loginhistory(models.Model):
    userid = models.IntegerField()
    username = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)
    actionkind = models.CharField(max_length=30)

class checklisttemplte(models.Model):
    templteid = models.IntegerField()
    templtename = models.CharField(max_length=100)
    templtekind = models.CharField(max_length=30)
    createtime = models.DateTimeField(auto_now=True)
    formlist = models.CharField(max_length=1000)
    fileaddress = models.CharField(max_length=100)

class formfilelist(models.Model):
    formfileid = models.IntegerField()
    formfilename = models.CharField(max_length=100)
    formfilekind = models.CharField(max_length=30)
    createtime = models.DateTimeField(auto_now=True)
    formcantain = models.CharField(max_length=1000)
    fileaddress = models.CharField(max_length=100)
    uploader = models.CharField(max_length=30)
    filestatus = models.CharField(max_length=10)

