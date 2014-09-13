from django.db import models
from accounts.models import MyUser


class SyncLog(models.Model):
    user = models.OneToOneField(MyUser, related_name='sync_log')
    last_synced_at = models.DateTimeField()