from django.http import HttpResponse
import urllib
import json
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
    return dic["results"][0]["address_components"][0]["short_name"]


def check(request):
    lat = request.POST['lat']
    lng = request.POST['lon']
    # timestamp = request.POST['timestamp']
    street = getStreet(lat, lng)
    
    lat = float(lat)
    lng = float(lng)

    #if Incident.objects.filter(street=street).exists():
    #    return HttpResponse(content="Geisterfahrer auf " + street)
    #else:
    #    return HttpResponse()

    print 'checking for relevant incidents'
    if critical(lat,lng,street):
        return HttpResponse(content="Geisterfahrer auf deiner strasse:" + street)
    else:
        return HttpResponse()


       

def critical(lat,lng,street):
    relevantIncidents = Incident.objects.filter(street=street)
    
    # search for incidents less than 50 km
    collection = [i for i in relevantIncidents if distance( (i.lat,i.lng),(lat,lng)) < 50 ] 
    
    # 
    if collection:
        return True
    else:
        return False


