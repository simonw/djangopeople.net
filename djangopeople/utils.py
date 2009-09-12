import md5, datetime
from django.conf import settings

ORIGIN_DATE = datetime.date(2000, 1, 1)

hex_to_int = lambda s: int(s, 16)
int_to_hex = lambda i: hex(i).replace('0x', '')

def lost_url_for_user(username):
    days = int_to_hex((datetime.date.today() - ORIGIN_DATE).days)
    hash = md5.new(settings.SECRET_KEY + days + username).hexdigest()
    return '/recover/%s/%s/%s/' % (
        username, days, hash
    )

def hash_is_valid(username, days, hash):
    if md5.new(settings.SECRET_KEY + days + username).hexdigest() != hash:
        return False # Hash failed
    # Ensure days is within a week of today
    days_now = (datetime.date.today() - ORIGIN_DATE).days
    days_old = days_now - hex_to_int(days)
    if days_old < 7:
        return True
    else:
        return False

def simple_decorator(decorator):
    """This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied."""
    # From http://wiki.python.org/moin/PythonDecoratorLibrary
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator