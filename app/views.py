from django.http import HttpResponse
import urllib
import json
from app.models import Incident

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

    print 'af'
    if Incident.objects.filter(street=street).exists():
        return HttpResponse(content="Geisterfahrer auf " + street)
    else:
        return HttpResponse()
        


