import datetime
import urllib
import json
import warnings

from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache

from app.models import Incident
from lib.helpers import distance

def post(request):
    # print request.POST['lat'], request.POST['lon'], request.POST['timestamp']
    
    lat = request.POST['lat']
    lng = request.POST['lon']
    timestamp = request.POST['timestamp']

    print 'lat:', lat, 'lng:', lng, 'timestamp:', timestamp
    
    # lookup the street from googles api
    street = getStreet(lat, lng)
    print street

    # store the object in the database
    Incident.objects.create(lat=float(lat),lng=float(lng),street=street,timestamp=timestamp)

    return HttpResponse(content=street)


def getStreet(lat, lon):
    print "REQUEST", lat, lon
    cache_key = "street:%s,%s"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&sensor=true"
    filehandle = urllib.urlopen( url )
    dic = json.load( filehandle )
    if dic["status"] != "OK" or not dic["results"]:
        warnings.warn("Google Geocoding API did not return any results for (%s, %s)." % (lat, lon))
        return ""
#        import random; street = "A%d" % random.randrange(10)
    else:
        address_components = dic["results"][0]["address_components"]
        for i, component in enumerate(address_components):
            if "route" in component["types"]:
                break
        else:
            i = 0
        street = address_components[i]["short_name"]
    cache.set(cache_key, street)
    return street


def check(request):
    lat = request.POST['lat']
    lng = request.POST['lon']
    # timestamp = request.POST['timestamp']
    street = getStreet(lat, lng)

    lat = float(lat)
    lng = float(lng)

    relevant = [i for i in Incident.objects.filter(
        timestamp__gt = datetime.datetime.now()
        - datetime.timedelta(hours=settings.INCIDENT_DECAY_TIME))
        if distance((i.lat, i.lng), (lat, lng)) < settings.INCIDENT_MAX_DISTANCE]

    if not relevant:
        return HttpResponse()

    relevant = [i for i in relevant if i.street == street]
    if not relevant:
        return HttpResponse(content="warning")

    return HttpResponse(content=street)
