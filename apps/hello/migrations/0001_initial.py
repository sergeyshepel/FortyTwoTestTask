# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DBActionsLog'
        db.create_table(u'hello_dbactionslog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('date_of_action', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'hello', ['DBActionsLog'])
        
        # Adding model 'Person'
        db.create_table(u'hello_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date_of_birthday', self.gf('django.db.models.fields.DateField')()),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('person_pic', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('other_contacts', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'hello', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'hello_person')

        # Deleting model 'DBActionsLog'
        db.delete_table(u'hello_dbactionslog')


    models = {
        u'hello.dbactionslog': {
            'Meta': {'object_name': 'DBActionsLog'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date_of_action': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hello.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'date_of_birthday': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'person_pic': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']