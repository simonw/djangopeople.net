
from south.db import db
from django.db import models
from djangopeople.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PendingMembership'
        db.create_table('djangopeople_pendingmembership', (
            ('id', orm['djangopeople.pendingmembership:id']),
            ('user', orm['djangopeople.pendingmembership:user']),
            ('group', orm['djangopeople.pendingmembership:group']),
            ('created_at', orm['djangopeople.pendingmembership:created_at']),
            ('pending_type', orm['djangopeople.pendingmembership:pending_type']),
        ))
        db.send_create_signal('djangopeople', ['PendingMembership'])
        
        # Adding model 'Group'
        db.create_table('djangopeople_group', (
            ('id', orm['djangopeople.group:id']),
            ('name', orm['djangopeople.group:name']),
            ('slug', orm['djangopeople.group:slug']),
            ('description', orm['djangopeople.group:description']),
            ('website', orm['djangopeople.group:website']),
            ('is_open', orm['djangopeople.group:is_open']),
        ))
        db.send_create_signal('djangopeople', ['Group'])
        
        # Adding model 'Membership'
        db.create_table('djangopeople_membership', (
            ('id', orm['djangopeople.membership:id']),
            ('user', orm['djangopeople.membership:user']),
            ('group', orm['djangopeople.membership:group']),
            ('created_at', orm['djangopeople.membership:created_at']),
            ('is_admin', orm['djangopeople.membership:is_admin']),
        ))
        db.send_create_signal('djangopeople', ['Membership'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PendingMembership'
        db.delete_table('djangopeople_pendingmembership')
        
        # Deleting model 'Group'
        db.delete_table('djangopeople_group')
        
        # Deleting model 'Membership'
        db.delete_table('djangopeople_membership')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djangopeople.country': {
            'area_in_sq_km': ('django.db.models.fields.FloatField', [], {}),
            'bbox_east': ('django.db.models.fields.FloatField', [], {}),
            'bbox_north': ('django.db.models.fields.FloatField', [], {}),
            'bbox_south': ('django.db.models.fields.FloatField', [], {}),
            'bbox_west': ('django.db.models.fields.FloatField', [], {}),
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'fips_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True'}),
            'geoname_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_alpha3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True'}),
            'iso_numeric': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True'}),
            'languages': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_people': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'population': ('django.db.models.fields.IntegerField', [], {})
        },
        'djangopeople.countrysite': {
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'djangopeople.djangoperson': {
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_active_on_irc': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'machinetags': ('django.contrib.contenttypes.generic.GenericRelation', [], {'to': "orm['machinetags.MachineTaggedItem']"}),
            'openid_delegate': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'openid_server': ('django.db.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'profile_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'djangopeople.group': {
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['djangopeople.DjangoPerson']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'djangopeople.membership': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['djangopeople.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['djangopeople.DjangoPerson']"})
        },
        'djangopeople.pendingmembership': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pending_memberships'", 'to': "orm['djangopeople.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pending_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pending_memberships'", 'to': "orm['djangopeople.DjangoPerson']"})
        },
        'djangopeople.portfoliosite': {
            'contributor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.DjangoPerson']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'djangopeople.region': {
            'bbox_east': ('django.db.models.fields.FloatField', [], {}),
            'bbox_north': ('django.db.models.fields.FloatField', [], {}),
            'bbox_south': ('django.db.models.fields.FloatField', [], {}),
            'bbox_west': ('django.db.models.fields.FloatField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djangopeople.Country']"}),
            'flag': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'num_people': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'machinetags.machinetaggeditem': {
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'predicate': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['djangopeople']
