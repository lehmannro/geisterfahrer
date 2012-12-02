from django.conf.urls.defaults import patterns, include, url
from app.models import Incident
from django.conf import settings

import datetime


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'start.html'}),
    url(r'^input$', 'django.views.generic.simple.direct_to_template', {'template': 'input.html'}),
    # url(r'^incidents$', 'django.views.generic.simple.direct_to_template', {'template': 'incidents.html', 'extra_context': {'incidents': Incident.objects.all() } }), # does not work: evaluated only once !!!
   #Incident.objects.filter(timestamp__gt = datetime.datetime.now() - datetime.timedelta(hours=settings.INCIDENT_DECAY_TIME))} }),
   url(r'^incidents$', 'django.views.generic.list_detail.object_list', {'template_name': 'incidents.html', 'queryset': Incident.objects.all()} ),
    
    url(r'^new$', 'app.views.post'),
    
    url(r'^check$', 'app.views.check'),
    # url(r'^geisterfahrer/', include('geisterfahrer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
