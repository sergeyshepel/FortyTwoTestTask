# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Team'
        db.create_table(u'hello_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal(u'hello', ['Team'])

        # Adding M2M table for field team_members on 'Team'
        m2m_table_name = db.shorten_name(u'hello_team_team_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(orm[u'hello.team'], null=False)),
            ('person', models.ForeignKey(orm[u'hello.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['team_id', 'person_id'])


    def backwards(self, orm):
        # Deleting model 'Team'
        db.delete_table(u'hello_team')

        # Removing M2M table for field team_members on 'Team'
        db.delete_table(db.shorten_name(u'hello_team_team_members'))


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
        },
        u'hello.requests': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Requests'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ajax': ('django.db.models.fields.BooleanField', [], {}),
            'is_secure': ('django.db.models.fields.BooleanField', [], {}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'priority': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'remote_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'hello.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hello.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        }
    }

    complete_apps = ['hello']