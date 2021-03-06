import datetime
import urllib
import json
import warnings
import operator
import math

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
    timestamp = datetime.datetime.now()

    print 'lat:', lat, 'lng:', lng, 'timestamp:', timestamp
    
    # lookup the street from googles api
    street = getStreet(lat, lng)
    print street

    # store the object in the database
    Incident.objects.create(lat=float(lat),lng=float(lng),street=street,timestamp=timestamp)

    return HttpResponse(content=street)


def getStreet(lat, lon):
    cache_key = "street:%s,%s" % (lat, lon)
    cached = cache.get(cache_key)
    if cached:
        print "CACHE HIT"
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

def render_to_json(status, message=None):
    response = dict(status=status)
    if message:
        response['message'] = message
    return HttpResponse(
        content=json.dumps(response),
        mimetype="application/json",
    )

BY_TIMESTAMP = operator.attrgetter('timestamp')

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
      return render_to_json("OK")

    alertable = [i for i in relevant if i.street == street]
    print "CHECK", street
    if not alertable:
        return render_to_json("WARNING",
            max(relevant, key=BY_TIMESTAMP).street)

    if len(relevant) > 1:
        latest1, latest2 = sorted(relevant, key=BY_TIMESTAMP, reverse=True)[:2]

        alertvec = (latest1.lat - latest2.lat, latest1.lng - latest2.lng)
        myvec = (lat - latest2.lat, lng - latest2.lng)

        alertdist = math.sqrt(alertvec[0]**2 + alertvec[1]**2)
        mydist = math.sqrt(myvec[0]**2 + myvec[1]**2)

        dotproduct = alertvec[0]*myvec[0] + alertvec[1]*myvec[1]
        angle = math.acos(dotproduct * 1.0 / (alertdist * mydist))

        if alertdist < mydist and abs(math.degrees(angle)) > 90:
            return render_to_json("WARNING", latest2.street)

    return render_to_json("ALARM", street)
