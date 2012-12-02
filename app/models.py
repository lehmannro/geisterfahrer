from django.db import models


class Incident (models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    street = models.CharField(max_length=128)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return u"`%s' at %f,%f" % (self.street, self.lat, self.lng)
