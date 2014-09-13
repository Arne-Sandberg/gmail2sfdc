# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MyUser'
        db.create_table(u'accounts_myuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('email', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('picture_url', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'accounts', ['MyUser'])

        # Adding model 'Gmail'
        db.create_table(u'accounts_gmail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='gmail_auth', unique=True, to=orm['accounts.MyUser'])),
            ('credentials_json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'accounts', ['Gmail'])

        # Adding model 'Salesforce'
        db.create_table(u'accounts_salesforce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='salesforce_auth', unique=True, to=orm['accounts.MyUser'])),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'accounts', ['Salesforce'])


    def backwards(self, orm):
        # Deleting model 'MyUser'
        db.delete_table(u'accounts_myuser')

        # Deleting model 'Gmail'
        db.delete_table(u'accounts_gmail')

        # Deleting model 'Salesforce'
        db.delete_table(u'accounts_salesforce')


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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'salesforce_auth'", 'unique': 'True', 'to': u"orm['accounts.MyUser']"})
        }
    }

    complete_apps = ['accounts']