
from south.db import db
from django.db import models
from djangopeople.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('djangopeople_region', (
            ('id', orm['djangopeople.Region:id']),
            ('code', orm['djangopeople.Region:code']),
            ('name', orm['djangopeople.Region:name']),
            ('country', orm['djangopeople.Region:country']),
            ('flag', orm['djangopeople.Region:flag']),
            ('bbox_west', orm['djangopeople.Region:bbox_west']),
            ('bbox_north', orm['djangopeople.Region:bbox_north']),
            ('bbox_east', orm['djangopeople.Region:bbox_east']),
            ('bbox_south', orm['djangopeople.Region:bbox_south']),
            ('num_people', orm['djangopeople.Region:num_people']),
        ))
        db.send_create_signal('djangopeople', ['Region'])
        
        # Adding model 'CountrySite'
        db.create_table('djangopeople_countrysite', (
            ('id', orm['djangopeople.CountrySite:id']),
            ('title', orm['djangopeople.CountrySite:title']),
            ('url', orm['djangopeople.CountrySite:url']),
            ('country', orm['djangopeople.CountrySite:country']),
        ))
        db.send_create_signal('djangopeople', ['CountrySite'])
        
        # Adding model 'Country'
        db.create_table('djangopeople_country', (
            ('id', orm['djangopeople.Country:id']),
            ('name', orm['djangopeople.Country:name']),
            ('iso_code', orm['djangopeople.Country:iso_code']),
            ('iso_numeric', orm['djangopeople.Country:iso_numeric']),
            ('iso_alpha3', orm['djangopeople.Country:iso_alpha3']),
            ('fips_code', orm['djangopeople.Country:fips_code']),
            ('continent', orm['djangopeople.Country:continent']),
            ('capital', orm['djangopeople.Country:capital']),
            ('area_in_sq_km', orm['djangopeople.Country:area_in_sq_km']),
            ('population', orm['djangopeople.Country:population']),
            ('currency_code', orm['djangopeople.Country:currency_code']),
            ('languages', orm['djangopeople.Country:languages']),
            ('geoname_id', orm['djangopeople.Country:geoname_id']),
            ('bbox_west', orm['djangopeople.Country:bbox_west']),
            ('bbox_north', orm['djangopeople.Country:bbox_north']),
            ('bbox_east', orm['djangopeople.Country:bbox_east']),
            ('bbox_south', orm['djangopeople.Country:bbox_south']),
            ('num_people', orm['djangopeople.Country:num_people']),
        ))
        db.send_create_signal('djangopeople', ['Country'])
        
        # Adding model 'PortfolioSite'
        db.create_table('djangopeople_portfoliosite', (
            ('id', orm['djangopeople.PortfolioSite:id']),
            ('title', orm['djangopeople.PortfolioSite:title']),
            ('url', orm['djangopeople.PortfolioSite:url']),
            ('contributor', orm['djangopeople.PortfolioSite:contributor']),
        ))
        db.send_create_signal('djangopeople', ['PortfolioSite'])
        
        # Adding model 'DjangoPerson'
        db.create_table('djangopeople_djangoperson', (
            ('id', orm['djangopeople.DjangoPerson:id']),
            ('user', orm['djangopeople.DjangoPerson:user']),
            ('bio', orm['djangopeople.DjangoPerson:bio']),
            ('country', orm['djangopeople.DjangoPerson:country']),
            ('region', orm['djangopeople.DjangoPerson:region']),
            ('latitude', orm['djangopeople.DjangoPerson:latitude']),
            ('longitude', orm['djangopeople.DjangoPerson:longitude']),
            ('location_description', orm['djangopeople.DjangoPerson:location_description']),
            ('photo', orm['djangopeople.DjangoPerson:photo']),
            ('profile_views', orm['djangopeople.DjangoPerson:profile_views']),
            ('openid_server', orm['djangopeople.DjangoPerson:openid_server']),
            ('openid_delegate', orm['djangopeople.DjangoPerson:openid_delegate']),
            ('last_active_on_irc', orm['djangopeople.DjangoPerson:last_active_on_irc']),
        ))
        db.send_create_signal('djangopeople', ['DjangoPerson'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('djangopeople_region')
        
        # Deleting model 'CountrySite'
        db.delete_table('djangopeople_countrysite')
        
        # Deleting model 'Country'
        db.delete_table('djangopeople_country')
        
        # Deleting model 'PortfolioSite'
        db.delete_table('djangopeople_portfoliosite')
        
        # Deleting model 'DjangoPerson'
        db.delete_table('djangopeople_djangoperson')
        
    
    
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
