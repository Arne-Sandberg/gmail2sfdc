# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Salesforce.sf_used_id'
        db.add_column(u'accounts_salesforce', 'sf_used_id',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Salesforce.sf_used_id'
        db.delete_column(u'accounts_salesforce', 'sf_used_id')


    models = {
        u'accounts.gmail': {
            'Meta': {'object_name': 'Gmail'},
            'credentials_json': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'gmail_auth'", 'unique': 'True', 'to': u"orm['accounts.MyUser']"})
        },
        u'accounts.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'picture_url': ('django.db.models.fields.TextField', [], {})
        },
        u'accounts.salesforce': {
            'Meta': {'object_name': 'Salesforce'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sf_used_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'salesforce_auth'", 'unique': 'True', 'to': u"orm['accounts.MyUser']"})
        }
    }

    complete_apps = ['accounts']