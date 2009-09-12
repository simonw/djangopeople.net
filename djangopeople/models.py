from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from machinetags.models import MachineTaggedItem, add_machinetag
from django.contrib.contenttypes import generic
from geopy import distance
from django.utils.safestring import mark_safe
from django.utils.html import escape
import tagging

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
    'companies active create'
).split())

class CountryManager(models.Manager):
    def top_countries(self):
        return self.get_query_set().order_by('-num_people')

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
        return self.region_set.order_by('-num_people')
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Countries'
    
    def __unicode__(self):
        return self.name
    
class Region(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)
    flag = models.CharField(max_length=100, blank=True)
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
        "Returns the nearest X people"
        # TODO: use this shonky SQL query instead of the other shonky method
        # From http://code.google.com/apis/maps/articles/phpsqlsearch_v3.html
        sql = """
            SELECT id, (
                3959 * acos(
                    cos(radians(%(latitude)s)) * 
                    cos(radians(latitude)) * 
                    cos(
                        radians(longitude) - radians(%(longitude)s)
                    )
                    + sin(radians(%(latitude)s)) * 
                    sin(radians(latitude))
                )
            ) AS distance
            FROM djangopeople_djangoperson
            HAVING distance < 100 ORDER BY distance LIMIT 0, %(num)s
        """
        # To search by kilometers instead of miles, replace 3959 with 6371.
        
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
        return unicode(self.user.get_full_name() or self.user.username)
    
    def get_absolute_url(self):
        return '/%s/' % self.user.username
    
    def save(self, force_insert=False, force_update=False): # TODO: Put in transaction
        # Update country and region counters
        super(DjangoPerson, self).save(force_insert=False, force_update=False)
        self.country.num_people = self.country.djangoperson_set.count()
        self.country.save()
        if self.region:
            self.region.num_people = self.region.djangoperson_set.count()
            self.region.save()
    
    class Meta:
        verbose_name_plural = 'Django people'

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
    
class CountrySite(models.Model):
    "Community sites for various countries"
    title = models.CharField(max_length = 100)
    url = models.URLField(max_length = 255)
    country = models.ForeignKey(Country)
    
    def __unicode__(self):
        return '%s <%s>' % (self.title, self.url)

class Group(models.Model):
    name = models.CharField(max_length = 255)
    slug = models.SlugField(max_length = 50)
    description = models.TextField(blank=True)
    website = models.URLField(verify_exists=False, blank=True)
    members = models.ManyToManyField(DjangoPerson,
        through='Membership', related_name='groups'
    )
    is_open = models.BooleanField(default = False, help_text = """
    Anyone can join an open group - otherwise, you will need to approve new members.
    """.strip())
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return u'/groups/%s/' % self.slug

class Membership(models.Model):
    user = models.ForeignKey(DjangoPerson, related_name = 'memberships')
    group = models.ForeignKey(Group, related_name = 'memberships')
    created_at = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)

    def __unicode__(self):
        if self.is_admin:
            return u'%s is an admin for %s' % (self.user, self.group)
        else:
            return u'%s is a member of %s' % (self.user, self.group)

class PendingMembership(models.Model):
    user = models.ForeignKey(DjangoPerson, related_name = 'pending_memberships')
    group = models.ForeignKey(Group, related_name = 'pending_memberships')
    created_at = models.DateTimeField(auto_now_add = True)
    pending_type = models.CharField(max_length = 10, choices = (
        ('invitation', 'Invitation'),
        ('request', 'Membership request')
    ))

    def __unicode__(self):
        if self.pending_type == 'invitation':
            return u'%s is invited to join %s' % (self.user, self.group)
        else:
            return u'%s has requested to join %s' % (self.user, self.group)


#class ClusteredPoint(models.Model):
#    
#    """
#    Represents a clustered point on the map. Each cluster is at a lat/long,
#    is only for one zoom level, and has a number of people.
#    If it is only one person, it is also associated with a DjangoPerson ID.
#    """
#    
#    latitude = models.FloatField()
#    longitude = models.FloatField()
#    zoom = models.IntegerField()
#    number = models.IntegerField()
#    djangoperson = models.ForeignKey(DjangoPerson, blank=True, null=True)
#    
#    def __unicode__(self):
#        return "%s people at (%s,%s,z%s)" % (self.number, self.longitude, self.latitude, self.zoom)
#    
#    class Admin:
#        list_display = ("zoom", "latitude", "longitude", "number")
#        ordering = ("zoom",)
