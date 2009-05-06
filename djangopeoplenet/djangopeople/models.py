from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from machinetags.models import MachineTaggedItem, add_machinetag
import tagging
from django.contrib.contenttypes import generic
from lib.geopy import distance
from django.utils.safestring import mark_safe
from django.utils.html import escape

RESERVED_USERNAMES = set((
    # Trailing spaces are essential in these strings, or split() will be buggy
    'feed www help security porn manage smtp fuck pop manager api owner shit '
    'secure ftp discussion blog features test mail email administrator '
    'xmlrpc web xxx pop3 abuse atom complaints news information imap cunt rss '
    'info pr0n about forum admin weblog team feeds root about info news blog '
    'forum features discussion email abuse complaints map skills tags ajax '
    'comet poll polling thereyet filter search zoom machinetags search django '
    'people profiles profile person navigate nav browse manage static css img '
    'javascript js code flags flag country countries region place places '
    'photos owner maps upload geocode geocoding login logout openid openids '
    'recover lost signup reports report flickr upcoming mashups recent irc '
    'group groups bulletin bulletins messages message newsfeed events company '
    'companies active'
).split())

class CountryManager(models.Manager):
    def top_countries(self):
        # Returns populated countries in order of population
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                djangopeople_country.id, count(*) AS peoplecount
            FROM
                djangopeople_djangoperson, djangopeople_country
            WHERE
                djangopeople_country.id = djangopeople_djangoperson.country_id
            GROUP BY country_id
            ORDER BY peoplecount DESC
        """)
        rows = cursor.fetchall()
        found = self.in_bulk([r[0] for r in rows])
        countries = []
        for row in rows:
            country = found[row[0]]
            country.peoplecount = row[1]
            countries.append(country)
        return countries

class Country(models.Model):
    # Longest len('South Georgia and the South Sandwich Islands') = 44
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2, unique=True)
    iso_numeric = models.CharField(max_length=3, unique=True)
    iso_alpha3 = models.CharField(max_length=3, unique=True)
    fips_code = models.CharField(max_length=2, unique=True)
    continent = models.CharField(max_length=2)
    # Longest len('Grand Turk (Cockburn Town)') = 26
    capital = models.CharField(max_length=30, blank=True)
    area_in_sq_km = models.FloatField()
    population = models.IntegerField()
    currency_code = models.CharField(max_length=3)
    # len('en-IN,hi,bn,te,mr,ta,ur,gu,ml,kn,or,pa,as,ks,sd,sa,ur-IN') = 56
    languages = models.CharField(max_length=60)
    geoname_id = models.IntegerField()

    # Bounding boxes
    bbox_west = models.FloatField()
    bbox_north = models.FloatField()
    bbox_east = models.FloatField()
    bbox_south = models.FloatField()
    
    # De-normalised
    num_people = models.IntegerField(default=0)
    
    objects = CountryManager()
    
    def top_regions(self):
        # Returns populated regions in order of population
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                djangopeople_region.id, count(*) AS peoplecount
            FROM
                djangopeople_djangoperson, djangopeople_region
            WHERE
                djangopeople_region.id = djangopeople_djangoperson.region_id
            AND
                djangopeople_region.country_id = %d
            GROUP BY djangopeople_djangoperson.region_id
            ORDER BY peoplecount DESC
        """ % self.id)
        rows = cursor.fetchall()
        found = Region.objects.in_bulk([r[0] for r in rows])
        regions = []
        for row in rows:
            region = found[row[0]]
            region.peoplecount = row[1]
            regions.append(region)
        return regions
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass

class Region(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)
    flag = models.CharField(max_length=100, blank=True)
    
#    geoname_id = models.IntegerField()
    bbox_west = models.FloatField()
    bbox_north = models.FloatField()
    bbox_east = models.FloatField()
    bbox_south = models.FloatField()
    
    # De-normalised
    num_people = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.country.iso_code.lower(), self.code.lower())
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
    
    class Admin:
        pass

class DjangoPerson(models.Model):
    user = models.ForeignKey(User, unique=True)
    bio = models.TextField(blank=True)
    
    # Location stuff - all location fields are required
    country = models.ForeignKey(Country)
    region = models.ForeignKey(Region, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_description = models.CharField(max_length=50)
    
    # Profile photo
    photo = models.ImageField(blank=True, upload_to='profiles')
    
    # Stats
    profile_views = models.IntegerField(default=0)
    
    # Machine tags
    machinetags = generic.GenericRelation(MachineTaggedItem)
    add_machinetag = add_machinetag
    
    # OpenID delegation
    openid_server = models.URLField(max_length=255, blank=True)
    openid_delegate = models.URLField(max_length=255, blank=True)

    # Last active on IRC
    last_active_on_irc = models.DateTimeField(blank=True, null=True)

    def irc_nick(self):
        try:
            return self.machinetags.filter(namespace = 'im', predicate='django')[0].value
        except IndexError:
            return '<none>'
     
    def get_nearest(self, num=5):
        "Returns the nearest X people, but only within the same continent"
        # TODO: Add caching
        
        people = list(self.country.djangoperson_set.select_related().exclude(pk=self.id))
        if len(people) <= num:
            # Not enough in country; use people from the same continent instead
            people = list(DjangoPerson.objects.filter(
                country__continent = self.country.continent,
            ).exclude(pk=self.id).select_related())

        # Sort and annotate people by distance
        for person in people:
            person.distance_in_miles = distance.VincentyDistance(
                (self.latitude, self.longitude),
                (person.latitude, person.longitude)
            ).miles
        
        # Return the nearest X
        people.sort(key=lambda x: x.distance_in_miles)
        return people[:num]
    
    def location_description_html(self):
        region = ''
        if self.region:
            region = '<a href="%s">%s</a>' % (
                self.region.get_absolute_url(), self.region.name
            )
            bits = self.location_description.split(', ')        
            if len(bits) > 1 and bits[-1] == self.region.name:
                bits[-1] = region
            else:
                bits.append(region)
                bits[:-1] = map(escape, bits[:-1])
            return mark_safe(', '.join(bits))
        else:
            return self.location_description
    
    def __unicode__(self):
        return unicode(self.user.get_full_name())
    
    def get_absolute_url(self):
        return '/%s/' % self.user.username
    
    def save(self): # TODO: Put in transaction
        # Update country and region counters
        super(DjangoPerson, self).save()
        self.country.num_people = self.country.djangoperson_set.count()
        self.country.save()
        if self.region:
            self.region.num_people = self.region.djangoperson_set.count()
            self.region.save()
    
    class Meta:
        verbose_name_plural = 'Django people'

    class Admin:
        list_display = ('user', 'profile_views')

    def irc_tracking_allowed(self):
        return not self.machinetags.filter(
            namespace = 'privacy', predicate='irctrack', value='private'
        ).count()

tagging.register(DjangoPerson,
    tag_descriptor_attr = 'skilltags',
    tagged_item_manager_attr = 'skilltagged'
)

class PortfolioSite(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=255)
    contributor = models.ForeignKey(DjangoPerson)
    
    def __unicode__(self):
        return '%s <%s>' % (self.title, self.url)
    
    class Admin:
        pass

class CountrySite(models.Model):
    "Community sites for various countries"
    title = models.CharField(max_length = 100)
    url = models.URLField(max_length = 255)
    country = models.ForeignKey(Country)
    
    def __unicode__(self):
        return '%s <%s>' % (self.title, self.url)
   
    class Admin:
        pass

def import_countries(fp):
    try:
        from xml.etree import cElementTree as ET
    except ImportError:
        from elementtree import ElementTree as ET
    et = ET.parse(fp)
    
    mapping = (
        # XML name, model field name, optional type conversion function
        ('countryName', 'name'),
        ('countryCode', 'iso_code'),
        ('isoNumeric', 'iso_numeric'),
        ('isoAlpha3', 'iso_alpha3'),
        ('fipsCode', 'fips_code'),
        ('continent', 'continent'),
        ('capital', 'capital'),
        ('areaInSqKm', 'area_in_sq_km', float),
        ('population', 'population', int),
        ('currencyCode', 'currency_code'),
        ('languages', 'languages'),
        ('geonameId', 'geoname_id', int),
        ('bBoxWest', 'bbox_west', float),
        ('bBoxNorth', 'bbox_north', float),
        ('bBoxEast', 'bbox_east', float),
        ('bBoxSouth', 'bbox_south', float),
    )
    mapping = [(tup + (unicode,))[:3] for tup in mapping]
    
    for country in et.findall('country'):
        creation_args = {}
        for xml, db_field, conv in mapping:
            if country.find(xml) is None or country.find(xml).text is None:
                continue
            creation_args[db_field] = conv(country.find(xml).text)
        
        Country.objects.get_or_create(iso_code = creation_args['iso_code'], 
            defaults = creation_args)

def import_us_states():
    """
    This file:
    http://www.census.gov/geo/cob/bdy/st/st00ascii/st99_d00_ascii.zip
    From here: http://www.census.gov/geo/www/cob/ascii_info.html
    
    Contains two files with shapes of the states in easy parse format - just 
    need to parse and find max and min lat and lon to get bounding boxes.
    """
    import os
    from django.contrib.localflavor.us.us_states import STATE_CHOICES
    REVERSE_STATE_CHOICES = dict([(p[1], p[0]) for p in STATE_CHOICES])
    
    # First collect all the segments
    s = open('djangopeople/data/st99_d00.dat').read()
    segments = [seg.strip() for seg in s.split('END') if seg.strip()]
    segment_lookup = {}
    for segment in segments:
        points = segment.split()
        id = points.pop(0)
        points = map(float, points)
        lats = points[::2] # Odd numbered indices
        lons = points[1::2] # Even numbered indices
        segment_lookup[id] = (lats, lons)
    
    # Now find out which segments belong to which US State
    s = open('djangopeople/data/st99_d00a.dat').read()
    chunks = [chunk.strip() for chunk in s.split('\n \n') if chunk.strip()]
    # Each chunk descripbes the corresponding segment
    assert len(chunks) == len(segments)
    
    # We're only going to add states which occur in both STATE_CHOICES and the
    # chunk/segment data
    
    statename_chunks = {}
    for chunk in chunks:
        bits = chunk.split('\n')
        chunk_id = bits[0]
        statename = bits[2].replace('"', '').strip()
        if not statename:
            continue # There's a blank one in there for some reason
        statename_chunks.setdefault(statename, []).append(chunk_id)
    
    usa = Country.objects.get(iso_code = 'US')
    
    for statename in statename_chunks.keys():
        if statename not in REVERSE_STATE_CHOICES:
            continue
        
        statecode = REVERSE_STATE_CHOICES[statename]
        if Region.objects.filter(
            country__iso_code = 'US', code = statecode
        ).count() > 0:
            continue # This state already exists
        
        # Find all the latitude / longitude values for the state
        segment_ids = statename_chunks[statename]
        lats = []
        lons = []
        for segment_id in segment_ids:
            lats.extend(segment_lookup[segment_id][0])
            lons.extend(segment_lookup[segment_id][1])
        
        bbox_south = min(lons)
        bbox_north = max(lons)
        bbox_west = min(lats)
        bbox_east = max(lats)
        
        flag = ''
        if os.path.exists(os.path.join(
            settings.OUR_ROOT, 'static/img/flags/us-states',
            '%s.png' % statecode.lower()
        )):
            flag = 'img/flags/us-states/%s.png' % statecode.lower()
        
        # And save the state
        Region.objects.create(
            country = usa,
            code = statecode,
            name = statename,
            bbox_south = bbox_south,
            bbox_north = bbox_north,
            bbox_west = bbox_west,
            bbox_east = bbox_east,
            flag = flag
        )


class ClusteredPoint(models.Model):
    
    """
    Represents a clustered point on the map. Each cluster is at a lat/long,
    is only for one zoom level, and has a number of people.
    If it is only one person, it is also associated with a DjangoPerson ID.
    """
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    number = models.IntegerField()
    djangoperson = models.ForeignKey(DjangoPerson, blank=True, null=True)
    
    class Admin:
        pass
