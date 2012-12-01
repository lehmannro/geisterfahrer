import datetime
import urllib
import json

from django.conf import settings
from django.http import HttpResponse

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


def getStreet(lat,lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&sensor=true"
    filehandle = urllib.urlopen( url )
    dic = json.load( filehandle )
    address_components = dic["results"][0]["address_components"]
    for i, component in enumerate(address_components):
        if "route" in component["types"]:
            break
    else:
        i = 0
    return address_components[i]["short_name"]


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
