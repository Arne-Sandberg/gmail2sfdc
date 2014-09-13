# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SyncLog'
        db.create_table(u'zaps_synclog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='sync_log', unique=True, to=orm['accounts.MyUser'])),
            ('last_synced_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'zaps', ['SyncLog'])


    def backwards(self, orm):
        # Deleting model 'SyncLog'
        db.delete_table(u'zaps_synclog')


    models = {
        u'accounts.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'picture_url': ('django.db.models.fields.TextField', [], {})
        },
        u'zaps.synclog': {
            'Meta': {'object_name': 'SyncLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_synced_at': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'sync_log'", 'unique': 'True', 'to': u"orm['accounts.MyUser']"})
        }
    }

    complete_apps = ['zaps']