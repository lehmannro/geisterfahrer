from django.http import HttpResponse
import urllib
import json

def post(request):
    print request.POST['lat'], request.POST['lon']

    street = getStreet(request.POST['lat'], request.POST['lon'])

    res =  street["results"][0]["address_components"][0]["short_name"]
    print res
    
    return HttpResponse(content=res)


def getStreet(lat,lon):
    url = "http://maps.googleapis.com/maps/api/geocode/json?latlng="+lat+","+lon+"&sensor=true"
    filehandle = urllib.urlopen( url )
    dic = json.load( filehandle )
    return dic
