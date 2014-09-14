from django.db import models


class MyUser(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    picture_url = models.TextField()


class Gmail(models.Model):
    user = models.OneToOneField(MyUser, related_name='gmail_auth')
    credentials_json = models.TextField()
    #additionally it can have scopes


class Salesforce(models.Model):
    user = models.OneToOneField(MyUser, related_name='salesforce_auth')
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    sf_used_id = models.CharField(max_length=200)