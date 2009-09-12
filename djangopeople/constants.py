SERVICES = (
    # shortname, name, icon
    ('flickr', 'Flickr', '/static/img/services/flickr.png'),
    ('delicious', 'del.icio.us', '/static/img/services/delicious.png'),
    ('magnolia', 'Ma.gnolia.com', '/static/img/services/magnolia.png'),
    ('twitter', 'Twitter', '/static/img/services/twitter.png'),
    ('facebook', 'Facebook', '/static/img/services/facebook.png'),
    ('linkedin', 'LinkedIn', '/static/img/services/linkedin.png'),
    ('pownce', 'Pownce', '/static/img/services/pownce.png'),
    ('djangosnippets', 'djangosnippets.org', '/static/img/services/django.png'),
    ('djangosites', 'DjangoSites.org', '/static/img/services/django.png'),
)
SERVICES_DICT = dict([(r[0], r) for r in SERVICES])

IMPROVIDERS = (
    # shortname, name, icon
    ('aim', 'AIM', '/static/img/improviders/aim.png'),
    ('yim', 'Y!IM', '/static/img/improviders/yim.png'),
    ('gtalk', 'GTalk', '/static/img/improviders/gtalk.png'),
    ('msn', 'MSN', '/static/img/improviders/msn.png'),
    ('jabber', 'Jabber', '/static/img/improviders/jabber.png'),
    ('django', '#django IRC', '/static/img/services/django.png'),
)
IMPROVIDERS_DICT = dict([(r[0], r) for r in IMPROVIDERS])

# Convenience mapping from fields to machinetag (namespace, predicate)
MACHINETAGS_FROM_FIELDS = dict(
    [('service_%s' % shortname, ('services', shortname))
     for shortname, name, icon in SERVICES] + 
    [('im_%s' % shortname, ('im', shortname))
     for shortname, name, icon in IMPROVIDERS] + [
        ('privacy_search', ('privacy', 'search')),
        ('privacy_email', ('privacy', 'email')),
        ('privacy_im', ('privacy', 'im')),
        ('privacy_irctrack', ('privacy', 'irctrack')),
    ]
)
