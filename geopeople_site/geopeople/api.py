from django.http import HttpResponse, HttpResponseRedirect
import datetime
from machinetags.models import MachineTaggedItem
from django.conf import settings

def irc_lookup(request, irc_nick):
    try:
        person = MachineTaggedItem.objects.get(
            namespace = 'im', predicate = 'django', value = irc_nick
        ).content_object
    except MachineTaggedItem.DoesNotExist:
        return HttpResponse('no match', mimetype = 'text/plain')
    return HttpResponse(
        u'%s, %s, %s, http://djangopeople.net/%s/' % (person, person.location_description, person.country, person.user.username), mimetype = 'text/plain'
    )

def irc_redirect(request, irc_nick):
    try:
        person = MachineTaggedItem.objects.get(
            namespace = 'im', predicate = 'django', value = irc_nick
        ).content_object
    except MachineTaggedItem.DoesNotExist:
        return HttpResponse('no match', mimetype = 'text/plain')
    return HttpResponseRedirect(
        'http://djangopeople.net/%s/' % person.user.username
    )

def irc_spotted(request, irc_nick):
    if request.POST.get('sekrit', '') != settings.API_PASSWORD:
        return api_response('BAD_SEKRIT')
    
    try:
        person = MachineTaggedItem.objects.get(
            namespace = 'im', predicate = 'django', value = irc_nick
        ).content_object
    except MachineTaggedItem.DoesNotExist:
        return api_response('NO_MATCH')
    
    if not person.irc_tracking_allowed():
        return api_response('TRACKING_FORBIDDEN')
    
    first_time_seen = not person.last_active_on_irc
    
    person.last_active_on_irc = datetime.datetime.now()
    person.save()
    
    if first_time_seen:
        return api_response('FIRST_TIME_SEEN')
    else:
        return api_response('TRACKED')

def api_response(code):
    return HttpResponse(code, mimetype='text/plain')

