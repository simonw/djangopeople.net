#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (c) 2007, Dima Dogadaylo (www.mysoftparade.com)
# See also: http://www.mysoftparade.com/blog/django-profile-sql-performance/

import os
from os import path
import sys
from datetime import datetime
import re
import urlparse


_PATH_COLUMN = 'Path'

def profile(operations):
    """Do requested profile operations on each from requested apps."""
    debug('profile', options)
    import operator
    urls = get_urls(options.depth)
    print('Found %d urls.' % len(urls))
    info('urls', urls)
    
    for op in operations:
        results = []
        for url in urls:
            res = op(url)
            res[_PATH_COLUMN] = url
            results += [res]
        results.sort(key=operator.itemgetter(op.sort_key),\
                    reverse=getattr(op, 'reverse', False))
        keys = results[0].keys()
        keys.remove(_PATH_COLUMN)
        keys.insert(0, _PATH_COLUMN)    # ensure that path column is first
        # build report table
        report = [keys] + [[line[key] for key in keys] for line in results]
        print_report(op.name, report)

def check_status_codes(depth=3, ignore_codes=(200,)):
    """Try to load all known pages and return dictionary of failed pages."""
    failed_urls = {}
    urls = get_urls(depth)
    for url in urls:
        resp = _internal_request(url)
        if resp.status_code not in ignore_codes:
           failed_urls[url] = {'code': resp.status_code}
           if resp.status_code == 0:
               failed_urls[url]['error'] = resp.content
    return failed_urls
               
def props(**kwargs):
    def wrapper(func):
        def executor(*args, **kwargs):
            output = func(*args, **kwargs)
            return output
        for key, value in kwargs.items():
            setattr(executor, key, value)
        return executor
    return wrapper
        
@props(name='SQL queries usage', sort_key='SQL', reverse=True)
def profile_sql(url):
    """Find SQL queriers usage for each page"""
    if options.verbosity:
        print "profile_sql", url,
    from django.conf import settings
    old_debug = settings.DEBUG
    settings.DEBUG = True
    from django.db import connection
    connection.queries = []
    responce =_internal_request(url)
    if options.verbosity:
        print "%d SQL queries, status code: %s " %\
              (len(connection.queries), responce.status_code)
    if options.verbosity > 1:
        for query in connection.queries:
            print query['sql'], query['time']
    settings.DEBUG = old_debug
    return {'SQL': len(connection.queries), 'Status': responce.status_code}

@props(name='Page size', sort_key='Size, b', reverse=True)
def profile_size(url):
    """Find size of each page."""
    if options.verbosity:
        print "profile_size", url,
    responce =_internal_request(url)
    size = len(responce.content)
    img = link = 0
    if responce.status_code == 200:
        img = len(re.findall(r'<img.*?>', responce.content))
        link = len(re.findall(r'<link.*?>', responce.content))
    if options.verbosity:
        print ", size: %sKb, status code: %s " %\
              (size, responce.status_code)
    return {'Size, b': size, 'Status': responce.status_code,
            '<img>': img, '<link>': link}

def print_report(name, report):
    """Print report"""
    row_total = len(report)    
    col_total = len(report[0])
    #calculate max length of each column
    format = [reduce(max, [len(str(report[row][col])) for row in xrange(row_total)])\
              for col in xrange(col_total)]
    total_width = reduce(lambda x,y: x+y, format) + col_total - 1
    format = " ".join(["%%%ds" % width for width in format])
    print "*"*total_width
    print name
    print "*"*total_width
    for row in report:
        print format % tuple(row)
    print
       
def get_urls(depth=3, apps=None):
    urls = set(['/'])
    if options.read_urls:
        urls.update(get_predefined_pages(options.read_urls))
        info("%s: current len of urls=%s" % (options.read_urls, len(urls)))
        debug("\n---predefined urls", urls)
    if depth > 0:
        debug("\n---urls before get_model_urls()", urls)
        urls.update(get_model_urls())
    if depth > 1:
        urls.update(get_base_urls(urls))
    new_urls = urls
    while depth > 2 and new_urls:
        new_urls = get_urls_from_content(new_urls) - urls
        urls.update(new_urls)
        depth -= 1
        info("depth", depth, "new_urls", len(new_urls))
    if not options.all_urls:
        urls = remove_dublicated_views(urls)
    return list(urls)

def get_model_urls(apps = []):
    import operator
    from django.db.models import get_app, get_apps, get_models
    debug("get_model_urls", apps)
    # convert app labels to app modules
    apps = [get_app(app_label) for app_label in apps] or get_apps()
    # all models of all profiled apps
    classes = reduce(operator.add, [get_models(app) for app in apps])
    debug("all models:\n", classes)
    # remove classes without get_absolute_url()
    classes = [cls for cls in classes\
               if hasattr(cls, 'get_absolute_url') and\
               hasattr(cls.get_absolute_url, '__call__')]
    debug("models with get_absolute_url():\n", classes)
    urls = []
    for cls in classes:
        try:
            if cls._default_manager.count():
                url = cls._default_manager.filter()[0].get_absolute_url()
                debug(cls, " -> ", url)
                if url:
                    urls += [url]
        except Exception, e:
            error("Can't obtain url for %s: %s" % (cls, e))
    debug("get_model_urls(): ", urls)
    return urls

def is_valid_url(url):
    from django.core.urlresolvers import resolve
    try:
        resolve(url)
        return True
    except:
        return False
    
def get_base_urls(urls):
    """Returns also all valid parent urls for each url from urls"""
    import re
    debug("get_base_urls(): ", urls)    
    base_urls = set([re.sub(r"/[-\w\?=&%]+/?$", r"/", url) for url in urls])
    debug('base_urls', base_urls)
    base_urls = [url for url in base_urls if is_valid_url(url)]
    debug('valid base_urls', base_urls)
    return base_urls

def iter_page_urls(page, url):
    """ Parse page and generate embedded urls.
    >>> lines = ('<a href="/abs/url/"> <a name="name">',
    ... '<A class="klass" href="href"> <a\\nhref="new_line"> <a hRef="caSe">',
    ... '<a href="http://ext"> <a href="#anchor">  <a href=""></a>')
    >>> page = "\\n".join(lines)
    >>> [u for u in iter_page_urls(page, '/dir/')]
    ['/abs/url/', '/dir/href', '/dir/new_line', '/dir/caSe']
    """
    for i in re.finditer(r'<a[^>]*?href="(?P<href>[^"]*?)".*?>', page, re.I):
        href = i.group('href')
        # bypass external urls, anchors and empty string
        if not href or re.match('^(ftp|http[s]?)://.+|^#.*', href):
            continue
        if href and not href[0] == '/':
            from urlparse import urljoin
            href = urljoin(url, href)
        yield href
    
def get_urls_from_content(urls):
    """Returns link to resources contained inside pages."""
    debug('\nget_urls_from_content', urls)
    hrefs = set([])
    for url in urls:
        responce = _internal_request(url)
        if responce.status_code == 200:
            for path in iter_page_urls(responce.content, url):
                hrefs.add(path)
    debug('hrefs', hrefs)
    return hrefs

def remove_dublicated_views(hrefs):
    """Remove pages mapped to same view."""
    from django.core.urlresolvers import resolve, Resolver404
    
    resolvers = []
    unique_urls = []
    for href in hrefs:
        try:
            r = resolve(href)
            if not r:
                continue
        except Resolver404:
            continue
        view, args, kwargs = r[0], list(r[1]), r[2]        
        # resolve() don't return url mapping name, and when generic views are used
        # it's a problem, so we do this trick to find
        # "really" different generic views
        args = [arg for arg in args if arg not in href]
        kwargs = dict([k, v] for k, v in kwargs.items()\
                      if not isinstance(v, basestring) or v not in href)
        r = (view, args, kwargs)
        if r not in resolvers:
            resolvers += [r]
            unique_urls += [href]
    return unique_urls

def get_predefined_pages(fname):
    if os.path.exists(fname) and os.path.isfile(fname):
        f = None
        try:
            try:
                f = open(fname, 'rb')
                return [line.strip() for line in f]
            except Exception, e:
                sys.stderr.write("get_predefined_pages %s: %s" % (path, e))
        finally:
            close_file(f)
    return []
    
def _internal_request(url):
    """Request page with internal Django client."""
    from django.test.client import Client
    # many code assume request.META['REMOTE_ADDR'] and etc
    client = Client(REMOTE_ADDR="127.0.0.1", HTTP_HOST="localhost")
    try:
        resp = client.get(url)
    except Exception, e:
        error('url=%s error=%s' % (url, e))
        resp = type('object', (), {'status_code':0, 'content': str(e)})

    if resp.status_code in (500,) and options.save_errors:
        save_page(resp.content, url, options.save_errors)
    return resp


def save_page(page, url, dir):
    fname = url2path(url, dir)
    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    write_file(fname, page)

def url2path(url, dir):
    scheme, location, path, query, fragment = urlparse.urlsplit(url)
    if not path or path.endswith('/'):
        path += 'index.html'
    return os.path.join(dir, "_".join(path.split('/')))

def error(*args):
    for arg in args:
        print >>sys.stderr,  arg,
    print >>sys.stderr

def info(*args):
    if options.verbosity > 0:
        for arg in args:
            print arg,
        print
        
def debug(*args):
    if options.verbosity > 1:
        for arg in args:
            print arg,
        print

def write_file(path, content, mode = "wb"):
    """Write content to file and retunr True is writing was sucessfull."""
    f = None
    try:
        try:
            f = open(path, mode)
            f.write(content)
        except Exception, e:
            sys.stderr.write("write_file %s: %s" % (path, e))
            return False
    finally:
        close_file(f)
    return True
            
def close_file(f):
    """Close file and retunr True is file was closed."""
    try:
        if f:
            f.close()
        return True
    except Exception, e:
        sys.stderr.write("close_file %s: %s" % (f, e))
        return False

PROFILERS = {
    'sql': profile_sql,
    'size': profile_size,
}

_default_options = {'verbosity': 0, 
                    'read_urls': './profile-pages.txt',
                    'depth': 4, 'all_urls': False,
                    'test': False, 'save_errors': None}
# will be redefined if run from command line
options = type('DefaultOptions', (), _default_options)

_usage  =  """%prog [options] [app_name ...]"""

def execute_from_command_line(argv):
    from optparse import OptionParser
    parser = OptionParser(version='0.1', usage = _usage)
    parser.set_defaults(**_default_options)
    parser.add_option('--settings',
        help='Python path to settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.')
    parser.add_option('--pythonpath',
        help='Lets you manually add a directory the Python path, e.g. "/home/djangoprojects/myproject".')
    parser.add_option('--verbosity', action='store', dest='verbosity',
        type='choice', choices=['0', '1', '2'],
        help='Verbosity level; 0=minimal output, 1=normal output, 2=all output')
    parser.add_option('-a', '--all', action='store_true',\
                      dest='all_urls',
                      help='Profile all found urls without view checking.')
    parser.add_option('--test', action='store_true',\
                      dest='test', help='Run django-profile doctests.')
    parser.add_option('--check', action='store_true',\
                      dest='check', help='Check status codes and report broken pages.')
    parser.add_option('--depth', action='store', dest='depth',\
                      help='Logical url searching depth; 0,1,2,3')
    parser.add_option('--read_urls',
                      help='Optional file with paths of pages to profile. Default ./profile-pages.txt')
    parser.add_option('--save_errors',
                      help='Directory to save pages with 500 status code and other errors. No default.')
    global options
    options, args = parser.parse_args(argv[1:])

    if options.test:
        import doctest
        doctest.testmod()
        return
    
    try:
        profilers = args and [PROFILERS[ind] for ind in args] or PROFILERS.values()
    except Exception, e:
        parser.error("Invalid indicators==%s:%s" % (args, e))
    options.verbosity = int(options.verbosity)
    options.depth = int(options.depth)
    if options.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
    if options.pythonpath:
        sys.path.insert(0, options.pythonpath)
    if not options.settings and not options.pythonpath:
        # behave like a manage.py
        try:
            import settings # Assumed to be in the same directory.
        except ImportError:
            import sys
            sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r.\nYou'll have to run django-profile.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
            sys.exit(1)
        from django.core.management import setup_environ
        setup_environ(settings)
        
    if options.check:
        failed = check_status_codes()
        for url, reason in failed.items():
            print url, '->', reason
        return
    profile(profilers)
        
if __name__ == '__main__':
    execute_from_command_line(sys.argv)

