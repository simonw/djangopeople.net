try:
    from xml.etree import cElementTree as ET
except ImportError:
    from elementtree import ElementTree as ET

from models import Country, Region

def import_countries(fp):
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