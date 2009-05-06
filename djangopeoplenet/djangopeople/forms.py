from django import newforms as forms
from django.newforms.forms import BoundField
from django.db.models import ObjectDoesNotExist
from models import DjangoPerson, Country, Region, User, RESERVED_USERNAMES
from groupedselect import GroupedChoiceField
from constants import SERVICES, IMPROVIDERS
#from tagging.forms import TagField

def region_choices():
    # For use with GroupedChoiceField
    regions = list(Region.objects.select_related().order_by('country', 'name'))
    groups = [(False, (('', '---'),))]
    current_country = False
    current_group = []
    
    for region in regions:
        if region.country.name != current_country:
            if current_group:
                groups.append((current_country, current_group))
                current_group = []
            current_country = region.country.name
        current_group.append((region.code, region.name))
    if current_group:
        groups.append((current_country, current_group))
        current_group = []
    
    return groups

def not_in_the_atlantic(self):
    if self.cleaned_data.get('latitude', '') and self.cleaned_data.get('longitude', ''):
        lat = self.cleaned_data['latitude']
        lon = self.cleaned_data['longitude']
        if 43 < lat < 45 and -39 < lon < -33:
            raise forms.ValidationError("Drag and zoom the map until the crosshair matches your location")
    return self.cleaned_data['location_description']

class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Dynamically add the fields for IM providers / external services
        if 'openid' in kwargs:
            self.openid = True
            kwargs.pop('openid')
        else:
            self.openid = False
        
        super(SignupForm, self).__init__(*args, **kwargs)
        self.service_fields = []
        for shortname, name, icon in SERVICES:
            field = forms.URLField(
                max_length=255, required=False, label=name
            )
            self.fields['service_' + shortname] = field
            self.service_fields.append({
                'label': name,
                'shortname': shortname,
                'id': 'service_' + shortname,
                'icon': icon,
                'field': BoundField(self, field, 'service_' + shortname),
            })
        
        self.improvider_fields = []
        for shortname, name, icon in IMPROVIDERS:
            field = forms.CharField(
                max_length=50, required=False, label=name
            )
            self.fields['im_' + shortname] = field
            self.improvider_fields.append({
                'label': name,
                'shortname': shortname,
                'id': 'im_' + shortname,
                'icon': icon,
                'field': BoundField(self, field, 'im_' + shortname),
            })
    
    # Fields for creating a User object
    username = forms.RegexField('^[a-zA-Z0-9]+$', min_length=3, max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)
    
    # Fields for creating a DjangoPerson profile
    bio = forms.CharField(widget=forms.Textarea, required=False)
    blog = forms.URLField(required=False)
    
    country = forms.ChoiceField(choices = [('', '')] + [
        (c.iso_code, c.name) for c in Country.objects.all()
    ])
    latitude = forms.FloatField(min_value=-90, max_value=90)
    longitude = forms.FloatField(min_value=-180, max_value=180)
    location_description = forms.CharField(max_length=50)
    
    region = GroupedChoiceField(required=False, choices=region_choices())
    
    privacy_search = forms.ChoiceField(
        choices = (
            ('public', 
             'Allow search engines to index my profile page (recommended)'),
            ('private', "Don't allow search engines to index my profile page"),
        ), widget = forms.RadioSelect, initial='public'
    )
    privacy_email = forms.ChoiceField(
        choices = (
            ('public', 'Anyone can see my e-mail address'),
            ('private', 'Only logged-in users can see my e-mail address'),
            ('never', 'No one can ever see my e-mail address'),
        ), widget = forms.RadioSelect, initial='private'
    )
    privacy_im = forms.ChoiceField(
        choices = (
            ('public', 'Anyone can see my IM details'),
            ('private', 'Only logged-in users can see my IM details'),
        ), widget = forms.RadioSelect, initial='private'
    )
    privacy_irctrack = forms.ChoiceField(
        choices = (
            ('public', 'Keep track of the last time I was seen on IRC (requires your IRC nick)'),
            ('private', "Don't record the last time I was seen on IRC"),
        ), widget = forms.RadioSelect, initial='public'
    )
    looking_for_work = forms.ChoiceField(
        choices = (
            ('', 'Not looking for work at the moment'),
            ('freelance', 'Looking for freelance work'),
            ('full-time', 'Looking for full-time work'),
        ), required=False #, widget = forms.RadioSelect, initial=''
    )
    
    #skilltags = TagField(required=False)
    
    # Upload a photo is a separate page, because if validation fails we 
    # don't want to tell them to upload it all over again
    #   photo = forms.ImageField(required=False)
    
    # Fields used to create machinetags
    
    # Validation
    def clean_password1(self):
        "Only required if NO openid set for this form"
        if not self.openid and not self.cleaned_data.get('password1', ''):
            raise forms.ValidationError('Password is required')
        return self.cleaned_data['password1']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1.strip() and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data['password2']
    
    def clean_username(self):
        already_taken = 'That username is unavailable'
        username = self.cleaned_data['username'].lower()
        
        # No reserved usernames, or anything that looks like a 4 digit year 
        if username in RESERVED_USERNAMES or (len(username) == 4 and username.isdigit()):
            raise forms.ValidationError(already_taken)
        
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(already_taken)
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError('That e-mail is already in use')
        return email
    
    def clean_region(self):
        # If a region is selected, ensure it matches the selected country
        if self.cleaned_data['region']:
            try:
                region = Region.objects.get(
                    code = self.cleaned_data['region'],
                    country__iso_code = self.cleaned_data['country']
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    'The region you selected does not match the country'
                )
        return self.cleaned_data['region']

    clean_location_description = not_in_the_atlantic

class PhotoUploadForm(forms.Form):
    photo = forms.ImageField()

#class SkillsForm(forms.Form):
#    skills = TagField(label='Change skills')

class BioForm(forms.Form):
    bio = forms.CharField(widget=forms.Textarea, required=False)

class AccountForm(forms.Form):
    openid_server = forms.URLField(required=False)
    openid_delegate = forms.URLField(required=False)

class LocationForm(forms.Form):
    country = forms.ChoiceField(choices = [('', '')] + [
        (c.iso_code, c.name) for c in Country.objects.all()
    ])
    latitude = forms.FloatField(min_value=-90, max_value=90)
    longitude = forms.FloatField(min_value=-180, max_value=180)
    location_description = forms.CharField(max_length=50)
    
    region = GroupedChoiceField(required=False, choices=region_choices())
    
    def clean_region(self):
        # If a region is selected, ensure it matches the selected country
        if self.cleaned_data['region']:
            try:
                region = Region.objects.get(
                    code = self.cleaned_data['region'],
                    country__iso_code = self.cleaned_data['country']
                )
            except ObjectDoesNotExist:
                raise forms.ValidationError(
                    'The region you selected does not match the country'
                )
        return self.cleaned_data['region']
    
    clean_location_description = not_in_the_atlantic

class FindingForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Dynamically add the fields for IM providers / external services
        self.person = kwargs.pop('person') # So we can validate e-mail later
        super(FindingForm, self).__init__(*args, **kwargs)
        self.service_fields = []
        for shortname, name, icon in SERVICES:
            field = forms.URLField(
                max_length=255, required=False, label=name
            )
            self.fields['service_' + shortname] = field
            self.service_fields.append({
                'label': name,
                'shortname': shortname,
                'id': 'service_' + shortname,
                'icon': icon,
                'field': BoundField(self, field, 'service_' + shortname),
            })
        
        self.improvider_fields = []
        for shortname, name, icon in IMPROVIDERS:
            field = forms.CharField(
                max_length=50, required=False, label=name
            )
            self.fields['im_' + shortname] = field
            self.improvider_fields.append({
                'label': name,
                'shortname': shortname,
                'id': 'im_' + shortname,
                'icon': icon,
                'field': BoundField(self, field, 'im_' + shortname),
            })
    
    email = forms.EmailField()
    blog = forms.URLField(required=False)
    privacy_search = forms.ChoiceField(
        choices = (
            ('public', 
             'Allow search engines to index my profile page (recommended)'),
            ('private', "Don't allow search engines to index my profile page"),
        ), widget = forms.RadioSelect, initial='public'
    )
    privacy_email = forms.ChoiceField(
        choices = (
            ('public', 'Anyone can see my e-mail address'),
            ('private', 'Only logged-in users can see my e-mail address'),
            ('never', 'No one can ever see my e-mail address'),
        ), widget = forms.RadioSelect, initial='private'
    )
    privacy_im = forms.ChoiceField(
        choices = (
            ('public', 'Anyone can see my IM details'),
            ('private', 'Only logged-in users can see my IM details'),
        ), widget = forms.RadioSelect, initial='private'
    )
    privacy_irctrack = forms.ChoiceField(
        choices = (
            ('public', 'Keep track of the last time I was seen on IRC (requires your IRC nick)'),
            ('private', "Don't record the last time I was seen on IRC"),
        ), widget = forms.RadioSelect, initial='public'
    )
    looking_for_work = forms.ChoiceField(
        choices = (
            ('', 'Not looking for work at the moment'),
            ('freelance', 'Looking for freelance work'),
            ('full-time', 'Looking for full-time work'),
        ), required=False #, widget = forms.RadioSelect, initial=''
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(
            email = email
        ).exclude(djangoperson = self.person).count() > 0:
            raise forms.ValidationError('That e-mail is already in use')
        return email

class PortfolioForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Dynamically add the fields for IM providers / external services
        assert 'person' in kwargs, 'person is a required keyword argument'
        person = kwargs.pop('person')
        super(PortfolioForm, self).__init__(*args, **kwargs)
        self.portfolio_fields = []
        initial_data = {}
        num = 1
        for site in person.portfoliosite_set.all():
            url_field = forms.URLField(
                max_length=255, required=False, label='URL %d' % num
            )
            title_field = forms.CharField(
                max_length=100, required=False, label='Title %d' % num
            )
            self.fields['title_%d' % num] = title_field
            self.fields['url_%d' % num] = url_field
            self.portfolio_fields.append({
                'title_field': BoundField(self, title_field, 'title_%d' % num),
                'url_field': BoundField(self, url_field, 'url_%d' % num),
                'title_id': 'id_title_%d' % num,
                'url_id': 'id_url_%d' % num,
            })
            initial_data['title_%d' % num] = site.title
            initial_data['url_%d' % num] = site.url
            num += 1
        
        # Add some more empty ones
        for i in range(num, num + 3):
            url_field = forms.URLField(
                max_length=255, required=False, label='URL %d' % i
            )
            title_field = forms.CharField(
                max_length=100, required=False, label='Title %d' % i
            )
            self.fields['title_%d' % i] = title_field
            self.fields['url_%d' % i] = url_field
            self.portfolio_fields.append({
                'title_field': BoundField(self, title_field, 'title_%d' % i),
                'url_field': BoundField(self, url_field, 'url_%d' % i),
                'title_id': 'id_title_%d' % i,
                'url_id': 'id_url_%d' % i,
            })
        
        self.initial = initial_data
        
        # Add custom validator for each url field
        for key in [k for k in self.fields if k.startswith('url_')]:
            setattr(self, 'clean_%s' % key, make_validator(key, self))

def make_validator(key, form):
    def check():
        if form.cleaned_data.get(key.replace('url_', 'title_')) and \
            not form.cleaned_data.get(key):
            raise forms.ValidationError, 'You need to provide a URL'
        return form.cleaned_data.get(key)
    return check
