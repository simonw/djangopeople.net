from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class MachineTaggedItem(models.Model):
    "A machine tag on an item."
    namespace = models.CharField(max_length=50, db_index=True)
    predicate = models.CharField(max_length=50, db_index=True)
    value = models.CharField(max_length=255, db_index=True)
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ('namespace', 'predicate', 'value')

    def __unicode__(self):
        value = self.value
        if ' ' in value or '"' in value:
            value = '"%s"' % value.replace('"', r'\"')
        return '%s:%s=%s' % (self.namespace, self.predicate, value)

import re
_part_re = re.compile('^[a-z][a-z0-9_]*$')
_machinetag_re = re.compile('^([a-z][a-z0-9_]*):([a-z][a-z0-9_]*)=(.*)$')

def is_valid_part(part):
    "Checks string is a valid namespace or predicate"
    return bool(_part_re.match(part))

def parse_machinetag(namespace_or_fulltag, predicate=None, value=None):
    if predicate:
        assert value, 'If you provide a predicate you must also provide a value'
        assert is_valid_part(namespace_or_fulltag), 'namespace must be valid'
        assert is_valid_part(predicate), 'predicate must be valid'
        namespace = namespace_or_fulltag
    else:
        match = _machinetag_re.match(machinetag)
        assert match, 'machinetag must be of format namespace:predicate=value'
        namespace, predicate, value = match.groups()
        if value[0] == '"' or value[-1] == '"':
            assert value[0] == '"' and value[-1] == '"', \
                'If value is quoted, double quotes must occur at start AND end'
            value = value[1:-1]
            value = value.replace(r'\"', '"')
    return namespace, predicate, value

def tag_exists(*args):
    namespace, predicate, value = parse_machinetag(*args)
    return MachineTaggedItem.objects.filter(
        namespace = namespace,
        predicate = predicate,
        value = value
    ).count() > 0

def obj_for_tag(*args):
    namespace, predicate, value = parse_machinetag(*args)
    found = list(MachineTaggedItem.objects.filter(
        namespace = namespace,
        predicate = predicate,
        value = value
    ))
    if len(found) > 0:
        return found[0].content_object
    else:
        return False

def add_machinetag(obj, namespace_or_fulltag, predicate=None, value=None):
    if predicate:
        assert value, 'If you provide a predicate you must also provide a value'
        assert is_valid_part(namespace_or_fulltag), 'namespace must be valid'
        assert is_valid_part(predicate), 'predicate must be valid'
        namespace = namespace_or_fulltag
    else:
        namespace, predicate, value = parse_machinetag(namespace_or_fulltag)
    obj.machinetags.create(
        namespace = namespace,
        predicate = predicate,
        value = value
    )
