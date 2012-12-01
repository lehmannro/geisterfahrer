from django.http import HttpResponse

def post(request):
    print request.POST['lat'], request.POST['lon']
    return HttpResponse()
