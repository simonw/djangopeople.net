from django.http import Http404, HttpResponse, HttpResponseRedirect, \
    HttpResponseForbidden
from django.contrib import auth
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from djangopeople.models import DjangoPerson, Country, User, Region, PortfolioSite
from djangopeople import utils
from django_openidauth.models import associate_openid, UserOpenID
from tagging.models import Tag
from tagging.views import tagged_object_list
from tagging.utils import calculate_cloud, edit_string_for_tags
from machinetags.utils import tagdict
from machinetags.models import MachineTaggedItem
#from djangopeople.forms import SkillsForm
from djangopeople.forms import SignupForm, PhotoUploadForm, PortfolioForm, \
    BioForm, LocationForm, FindingForm, AccountForm
from djangopeople.constants import MACHINETAGS_FROM_FIELDS, IMPROVIDERS_DICT, SERVICES_DICT
from django.conf import settings
import os, md5, datetime
from PIL import Image
from cStringIO import StringIO

def render(request, template, context_dict=None):
    return render_to_response(
        template, context_dict or {}, context_instance=RequestContext(request)
    )

@utils.simple_decorator
def must_be_owner(view):
    def inner(request, *args, **kwargs):
        if not request.user or request.user.is_anonymous() \
            or request.user.username != args[0]:
            return HttpResponseForbidden('Not allowed')
        return view(request, *args, **kwargs)
    return inner

def index(request):
    recent_people = list(DjangoPerson.objects.all().select_related().order_by('-id')[:100])
    return render(request, 'index.html', {
        'recent_people': recent_people,
        'recent_people_limited': recent_people[:4],
        'total_people': DjangoPerson.objects.count(),
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'countries': Country.objects.top_countries(),
    })

def about(request):
    return render(request, 'about.html', {
        'total_people': DjangoPerson.objects.count(),
        'openid_users': User.objects.filter(useropenid__openid__startswith = 'http').distinct().count(),
        'countries': Country.objects.top_countries(),
    })

def recent(request):
    return render(request, 'recent.html', {
        'people': DjangoPerson.objects.all().select_related().order_by('-auth_user.date_joined')[:50],
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })

def login(request):
    if request.method != 'POST':
        return render(request, 'login.html', {
            'next': request.REQUEST.get('next', ''),
        })
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(
            request.POST.get('next', '/%s/' % user.username)
        )
    else:
        return render(request, 'login.html', {
            'is_invalid': True,
            'username': username, # Populate form
            'next': request.REQUEST.get('next', ''),
        })

def logout(request):
    auth.logout(request)
    request.session['openids'] = []
    return HttpResponseRedirect('/')

def lost_password(request):
    username = request.POST.get('username', '')
    if username:
        try:
            person = DjangoPerson.objects.get(user__username = username)
        except DjangoPerson.DoesNotExist:
            return render(request, 'lost_password.html', {
                'message': 'That was not a valid username.'
            })
        path = utils.lost_url_for_user(username)
        from django.core.mail import send_mail
        import smtplib
        body = render_to_string('recovery_email.txt', {
            'path': path,
            'person': person,
        })
        try:
            send_mail(
                'Django People account recovery', body,
                settings.RECOVERY_EMAIL_FROM, [person.user.email],
                fail_silently=False
            )
        except smtplib.SMTPException:
            return render(request, 'lost_password.html', {
                'message': 'Could not e-mail you a recovery link.',
            })
        return render(request, 'lost_password.html', {
            'message': ('An e-mail has been sent with instructions for '
                "recovering your account. Don't forget to check your spam "
                'folder!')
        })
    return render(request, 'lost_password.html')

def lost_password_recover(request, username, days, hash):
    user = get_object_or_404(User, username=username)
    if utils.hash_is_valid(username, days, hash):
        user.backend='django.contrib.auth.backends.ModelBackend' 
        auth.login(request, user)
        return HttpResponseRedirect('/%s/password/' % username)
    else:
        return render(request, 'lost_password.html', {
            'message': 'That was not a valid account recovery link'
        })

def openid_whatnext(request):
    """
    If user is already logged in, send them to /openid/associations/
    Otherwise, send them to the signup page
    """
    if not request.openid:
        return HttpResponseRedirect('/')
    if request.user.is_anonymous():
        # Have they logged in with an OpenID that matches an account?
        try:
            user_openid = UserOpenID.objects.get(openid = str(request.openid))
        except UserOpenID.DoesNotExist:
            return HttpResponseRedirect('/signup/')
        # Log the user in
        user = user_openid.user
        user.backend='django.contrib.auth.backends.ModelBackend' 
        auth.login(request, user)
        return HttpResponseRedirect('/%s/' % user.username)
    
    else:
        return HttpResponseRedirect('/openid/associations/')

def signup(request):
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if request.openid:
            form = SignupForm(
                request.POST, request.FILES, openid=request.openid
            )
        else:
            form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            # First create the user
            creation_args = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
            }
            if form.cleaned_data.get('password1'):
                creation_args['password'] = form.cleaned_data['password1']
                
            user = User.objects.create_user(**creation_args)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            
            if request.openid:
                associate_openid(user, str(request.openid))
            
            region = None
            if form.cleaned_data['region']:
                region = Region.objects.get(
                    country__iso_code = form.cleaned_data['country'],
                    code = form.cleaned_data['region']
                )
            
            # Now create the DjangoPerson
            person = DjangoPerson.objects.create(
                user = user,
                bio = form.cleaned_data['bio'],
                country = Country.objects.get(
                    iso_code = form.cleaned_data['country']
                ),
                region = region,
                latitude = form.cleaned_data['latitude'],
                longitude = form.cleaned_data['longitude'],
                location_description = form.cleaned_data['location_description']
            )
            
            # Set up the various machine tags
            for fieldname, (namespace, predicate) in \
                    MACHINETAGS_FROM_FIELDS.items():
                if form.cleaned_data.has_key(fieldname) and \
                    form.cleaned_data[fieldname].strip():
                    value = form.cleaned_data[fieldname].strip()
                    person.add_machinetag(namespace, predicate, value)
            
            # Stash their blog and looking_for_work
            if form.cleaned_data['blog']:
                person.add_machinetag(
                    'profile', 'blog', form.cleaned_data['blog']
                )
            if form.cleaned_data['looking_for_work']:
                person.add_machinetag(
                    'profile', 'looking_for_work',
                    form.cleaned_data['looking_for_work']
                )
            
            # Finally, set their skill tags
            person.skilltags = form.cleaned_data['skilltags']
            
            # Log them in and redirect to their profile page
            # HACK! http://groups.google.com/group/django-users/
            #    browse_thread/thread/39488db1864c595f
            user.backend='django.contrib.auth.backends.ModelBackend' 
            auth.login(request, user)
            return HttpResponseRedirect(person.get_absolute_url())
    else:
        if request.openid and request.openid.sreg:
            sreg = request.openid.sreg
            first_name = ''
            last_name = ''
            username = ''
            if sreg.get('fullname'):
                bits = sreg['fullname'].split()
                first_name = bits[0]
                if len(bits) > 1:
                    last_name = ' '.join(bits[1:])
            # Find a not-taken username
            if sreg.get('nickname'):
                username = derive_username(sreg['nickname'])
            form = SignupForm(initial = {
                'first_name': first_name,
                'last_name': last_name,
                'email': sreg.get('email', ''),
                'username': username,
            }, openid = request.openid)
        elif request.openid:
            form = SignupForm(openid = request.openid)
        else:
            form = SignupForm()
    
    return render(request, 'signup.html', {
        'form': form,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'openid': request.openid,
    })

import re
notalpha_re = re.compile('[^a-zA-Z0-9]')
def derive_username(nickname):
    nickname = notalpha_re.sub('', nickname)
    if not nickname:
        return ''
    base_nickname = nickname
    to_add = 1
    while True:
        try:
            DjangoPerson.objects.get(user__username = nickname)
        except DjangoPerson.DoesNotExist:
            break
        nickname = base_nickname + str(to_add)
        to_add += 1
    return nickname

@must_be_owner
def upload_profile_photo(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Figure out what type of image it is
            image_content = request.FILES['photo'].read()
            format = Image.open(StringIO(image_content)).format
            format = format.lower().replace('jpeg', 'jpg')
            filename = md5.new(image_content).hexdigest() + '.' + format
            # Save the image
            path = os.path.join(settings.MEDIA_ROOT, 'profiles', filename)
            open(path, 'w').write(image_content)
            person.photo = 'profiles/%s' % filename
            person.save()
            return HttpResponseRedirect('/%s/upload/done/' % username)
    else:
        form = PhotoUploadForm()
    return render(request, 'upload_profile_photo.html', {
        'form': form,
        'person': person,
    })

@must_be_owner
def upload_done(request, username):
    "Using a double redirect to try and stop back button from re-uploading"
    return HttpResponseRedirect('/%s/' % username)

def country(request, country_code):
    country = get_object_or_404(Country, iso_code = country_code.upper())
    return render(request, 'country.html', {
        'country': country,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'regions': country.top_regions(),
    })

def country_sites(request, country_code):
    country = get_object_or_404(Country, iso_code = country_code.upper())
    sites = PortfolioSite.objects.select_related().filter(
        contributor__country = country
    ).order_by('contributor')
    return render(request, 'country_sites.html', {
        'country': country,
        'sites': sites,
    })

def region(request, country_code, region_code):
    region = get_object_or_404(Region, 
        country__iso_code = country_code.upper(),
        code = region_code.upper()
    )
    return render(request, 'country.html', {
        'country': region,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })

def profile(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    person.profile_views += 1 # Not bothering with transactions; only a stat
    person.save()
    mtags = tagdict(person.machinetags.all())
    
    # Set up convenient iterables for IM and services
    ims = []
    for key, value in mtags.get('im', {}).items():
        shortname, name, icon = IMPROVIDERS_DICT.get(key, ('', '', ''))
        if not shortname:
            continue # Bad machinetag
        ims.append({
            'shortname': shortname,
            'name': name,
            'value': value,
        })
    ims.sort(lambda x, y: cmp(x['shortname'], y['shortname']))
    
    services = []
    for key, value in mtags.get('services', {}).items():
        shortname, name, icon = SERVICES_DICT.get(key, ('', '', ''))
        if not shortname:
            continue # Bad machinetag
        services.append({
            'shortname': shortname,
            'name': name,
            'value': value,
        })
    services.sort(lambda x, y: cmp(x['shortname'], y['shortname']))
    
    # Set up vars that control privacy stuff
    privacy = {
        'show_im': (
            mtags['privacy']['im'] == 'public' or 
            not request.user.is_anonymous()
        ),
        'show_email': (
            mtags['privacy']['email'] == 'public' or 
            (not request.user.is_anonymous() and mtags['privacy']['email'] == 'private')
        ),
        'hide_from_search': mtags['privacy']['search'] != 'public',
        'show_last_irc_activity': bool(person.last_active_on_irc and person.irc_tracking_allowed()),
    }
    
    # Should we show the 'Finding X' section at all?
    show_finding = services or privacy['show_email'] or \
        (privacy['show_im'] and ims)
    
    return render(request, 'profile.html', {
        'person': person,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'is_owner': request.user.username == username,
#        'skills_form': SkillsForm(initial={
#            'skills': edit_string_for_tags(person.skilltags)
#        }),
        'mtags': mtags,
        'ims': ims,
        'services': services,
        'privacy': privacy,
        'show_finding': show_finding,
    })

@must_be_owner
def edit_finding(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = FindingForm(request.POST, person=person)
        if form.is_valid():
            user = person.user
            user.email = form.cleaned_data['email']
            user.save()
            
            person.machinetags.filter(namespace = 'profile').delete()
            if form.cleaned_data['blog']:
                person.add_machinetag(
                    'profile', 'blog', form.cleaned_data['blog']
                )
            if form.cleaned_data['looking_for_work']:
                person.add_machinetag(
                    'profile', 'looking_for_work',
                    form.cleaned_data['looking_for_work']
                )
            
            for fieldname, (namespace, predicate) in \
                MACHINETAGS_FROM_FIELDS.items():
                person.machinetags.filter(
                    namespace = namespace, predicate = predicate
                ).delete()
                if form.cleaned_data.has_key(fieldname) and \
                    form.cleaned_data[fieldname].strip():
                    value = form.cleaned_data[fieldname].strip()
                    person.add_machinetag(namespace, predicate, value)
            
            return HttpResponseRedirect('/%s/' % username)
    else:
        mtags = tagdict(person.machinetags.all())
        initial = {
            'email': person.user.email,
            'blog': mtags['profile']['blog'],
            'looking_for_work': mtags['profile']['looking_for_work'],
        }
        
        # Fill in other initial fields from machinetags
        for fieldname, (namespace, predicate) in \
                MACHINETAGS_FROM_FIELDS.items():
            initial[fieldname] = mtags[namespace][predicate]
        
        form = FindingForm(initial=initial, person=person)
    return render(request, 'edit_finding.html', {
        'form': form,
        'person': person,
    })

@must_be_owner
def edit_portfolio(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, person = person)
        if form.is_valid():
            person.portfoliosite_set.all().delete()
            for key in [k for k in request.POST if k.startswith('title_')]:
                title = request.POST[key]
                url = request.POST[key.replace('title_', 'url_')]
                if title.strip() and url.strip():
                    person.portfoliosite_set.create(title = title, url = url)
            return HttpResponseRedirect('/%s/' % username)
    else:
        form = PortfolioForm(person = person)
    return render(request, 'edit_portfolio.html', {
        'form': form,
    })

@must_be_owner
def edit_account(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            person.openid_server = form.cleaned_data['openid_server']
            person.openid_delegate = form.cleaned_data['openid_delegate']
            person.save()
            return HttpResponseRedirect('/%s/' % username)
    else:
        form = AccountForm(initial = {
            'openid_server': person.openid_server,
            'openid_delegate': person.openid_delegate,
        })
    return render(request, 'edit_account.html', {
        'form': form,
        'person': person,
        'user': person.user,
    })

#@must_be_owner
#def edit_skills(request, username):
#    person = get_object_or_404(DjangoPerson, user__username = username)
#    if not request.POST.get('skills'):
#        return render(request, 'edit_skills.html', {
#            'form': SkillsForm(initial={
#                'skills': edit_string_for_tags(person.skilltags)
#            }),
#        })
#    person.skilltags = request.POST.get('skills', '')
#    return HttpResponseRedirect('/%s/' % username)

@must_be_owner
def edit_password(request, username):
    user = get_object_or_404(User, username = username)
    p1 = request.POST.get('password1', '')
    p2 = request.POST.get('password2', '')
    if p1 and p2 and p1 == p2:
        user.set_password(p1)
        user.save()
        return HttpResponseRedirect('/%s/' % username)
    else:
        return render(request, 'edit_password.html')

@must_be_owner
def edit_bio(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = BioForm(request.POST)
        if form.is_valid():
            person.bio = form.cleaned_data['bio']
            person.save()
            return HttpResponseRedirect('/%s/' % username)
    else:
        form = BioForm(initial = {'bio': person.bio})
    return render(request, 'edit_bio.html', {
        'form': form,
    })

@must_be_owner
def edit_location(request, username):
    person = get_object_or_404(DjangoPerson, user__username = username)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            region = None
            if form.cleaned_data['region']:
                region = Region.objects.get(
                    country__iso_code = form.cleaned_data['country'],
                    code = form.cleaned_data['region']
                )
            person.country = Country.objects.get(
                iso_code = form.cleaned_data['country']
            )
            person.region = region
            person.latitude = form.cleaned_data['latitude']
            person.longitude = form.cleaned_data['longitude']
            person.location_description = \
                form.cleaned_data['location_description']
            person.save()
            return HttpResponseRedirect('/%s/' % username)
    else:
        form = LocationForm()
    return render(request, 'edit_location.html', {
        'form': form,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })

def skill_cloud(request):
    tags = DjangoPerson.skilltags.cloud(steps=5)
    calculate_cloud(tags, 5)
    return render(request, 'skills.html', {
        'tags': tags
    })

def country_skill_cloud(request, country_code):
    country = get_object_or_404(Country, iso_code = country_code.upper())
    tags = Tag.objects.cloud_for_model(DjangoPerson, steps=5, filters={
        'country': country
    })
    calculate_cloud(tags, 5)
    return render(request, 'skills.html', {
        'tags': tags,
        'country': country
    })

def skill(request, tag):
    return tagged_object_list(request,
        model = DjangoPerson,
        tag = tag,
        related_tags = True,
        related_tag_counts = True,
        template_name = 'skill.html',
        extra_context = {
            'api_key': settings.GOOGLE_MAPS_API_KEY,
        },
    )

def country_skill(request, country_code, tag):
    return tagged_object_list(request,
        model = DjangoPerson,
        tag = tag,
        related_tags = True,
        related_tag_counts = True,
        extra_filter_args = {'country__iso_code': country_code.upper()},
        template_name = 'skill.html',
        extra_context = {
            'api_key': settings.GOOGLE_MAPS_API_KEY,
            'country': Country.objects.get(iso_code = country_code.upper()),
        },
    )

def country_looking_for(request, country_code, looking_for):
    country = get_object_or_404(Country, iso_code = country_code.upper())
    ids = [
        o['object_id'] for o in MachineTaggedItem.objects.filter(
        namespace='profile', predicate='looking_for_work', value=looking_for).values('object_id')
    ]
    people = DjangoPerson.objects.filter(country = country, id__in = ids)
    return render(request, 'country_looking_for.html', {
        'people': people,
        'country': country,
        'looking_for': looking_for,
    })

from django.db.models import Q
import operator

def search_people(q):
    words = [w.strip() for w in q.split() if len(w.strip()) > 2]
    if not words:
        return []
    
    terms = []
    for word in words:
        terms.append(Q(
            user__username__icontains = word) | 
            Q(user__first_name__icontains = word) | 
            Q(user__last_name__icontains = word)
        )
    
    combined = reduce(operator.and_, terms)
    return DjangoPerson.objects.filter(combined).select_related().distinct()
    
def search(request):
    q = request.GET.get('q', '')
    has_badwords = [
        w.strip() for w in q.split() if len(w.strip()) in (1, 2)
    ]
    if q:
        people = search_people(q)
        return render(request, 'search.html', {
            'q': q,
            'results': people,
            'api_key': settings.GOOGLE_MAPS_API_KEY,
            'has_badwords': has_badwords,
        })
    else:
        return render(request, 'search.html')

def irc_active(request):
    "People active on IRC in the last hour"
    results = DjangoPerson.objects.filter(
        last_active_on_irc__gt = 
            datetime.datetime.now() - datetime.timedelta(hours=1)
    ).order_by('-last_active_on_irc')
    # Filter out the people who don't want to be tracked (inefficient)
    results = [r for r in results if r.irc_tracking_allowed()]
    return render(request, 'irc_active.html', {
        'results': results,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
    })

# Custom variant of the generic view from django-tagging
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list
#from tagging.models import Tag, TaggedItem
#from tagging.utils import get_tag
#def tagged_object_list(request, model=None, tag=None, related_tags=False,
#        related_tag_counts=True, extra_filter_args=None, **kwargs):
#    """
#    A thin wrapper around
#    ``django.views.generic.list_detail.object_list`` which creates a
#    ``QuerySet`` containing instances of the given model tagged with
#    the given tag.
#
#    In addition to the context variables set up by ``object_list``, a
#    ``tag`` context variable will contain the ``Tag`` instance for the
#    tag.
#
#    If ``related_tags`` is ``True``, a ``related_tags`` context variable
#    will contain tags related to the given tag for the given model.
#    Additionally, if ``related_tag_counts`` is ``True``, each related
#    tag will have a ``count`` attribute indicating the number of items
#    which have it in addition to the given tag.
#    """
#    if model is None:
#        try:
#            model = kwargs['model']
#        except KeyError:
#            raise AttributeError(_('tagged_object_list must be called with a model.'))
#
#    if tag is None:
#        try:
#            tag = kwargs['tag']
#        except KeyError:
#            raise AttributeError(_('tagged_object_list must be called with a tag.'))
#
#    tag_instance = get_tag(tag)
#    if tag_instance is None:
#        raise Http404(_('No Tag found matching "%s".') % tag)
#    queryset = TaggedItem.objects.get_by_model(model, tag_instance)
#    if extra_filter_args:
#        queryset = queryset.filter(**extra_filter_args)
#    if not kwargs.has_key('extra_context'):
#        kwargs['extra_context'] = {}
#    kwargs['extra_context']['tag'] = tag_instance
#    if related_tags:
#        kwargs['extra_context']['related_tags'] = \
#            Tag.objects.related_for_model(tag_instance, model,
#                                          counts=related_tag_counts)
#    return object_list(request, queryset, **kwargs)
#