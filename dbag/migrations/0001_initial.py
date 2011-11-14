# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Metric'
        db.create_table('dbag_metric', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric_type_label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('metric_properties', self.gf('jsonfield.fields.JSONField')(default='{}')),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('unit_label', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('unit_label_plural', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('do_collect', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('dbag', ['Metric'])

        # Adding model 'DataSample'
        db.create_table('dbag_datasample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbag.Metric'])),
            ('utc_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.utcnow)),
            ('value', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal('dbag', ['DataSample'])

        # Adding model 'Dashboard'
        db.create_table('dbag_dashboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal('dbag', ['Dashboard'])

        # Adding model 'DashboardPanel'
        db.create_table('dbag_dashboardpanel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbag.Metric'])),
            ('dashboard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbag.Dashboard'])),
            ('do_display', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('show_sparkline', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
        ))
        db.send_create_signal('dbag', ['DashboardPanel'])

        # Adding unique constraint on 'DashboardPanel', fields ['metric', 'dashboard']
        db.create_unique('dbag_dashboardpanel', ['metric_id', 'dashboard_id'])


    def backwards(self, orm):
        
        # Deleting model 'Metric'
        db.delete_table('dbag_metric')

        # Deleting model 'DataSample'
        db.delete_table('dbag_datasample')

        # Deleting model 'Dashboard'
        db.delete_table('dbag_dashboard')

        # Deleting model 'DashboardPanel'
        db.delete_table('dbag_dashboardpanel')

        # Removing unique constraint on 'DashboardPanel', fields ['metric', 'dashboard']
        db.delete_unique('dbag_dashboardpanel', ['metric_id', 'dashboard_id'])


    models = {
        'dbag.dashboard': {
            'Meta': {'object_name': 'Dashboard'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'panels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['dbag.Metric']", 'through': "orm['dbag.DashboardPanel']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        'dbag.dashboardpanel': {
            'Meta': {'unique_together': "(('metric', 'dashboard'),)", 'object_name': 'DashboardPanel'},
            'dashboard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbag.Dashboard']"}),
            'do_display': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbag.Metric']"}),
            'show_sparkline': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'dbag.datasample': {
            'Meta': {'object_name': 'DataSample'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dbag.Metric']"}),
            'utc_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'value': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'dbag.metric': {
            'Meta': {'object_name': 'Metric'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'do_collect': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'metric_properties': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'metric_type_label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'unit_label': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'unit_label_plural': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['dbag']
