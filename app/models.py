from django.db import models
# from django.contrib.gis.db.models import PointField


# Create your models here.
class Incident (models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	# pos = PointField()
	street = models.CharField(max_length=128)
	timestamp = models.DateTimeField()


