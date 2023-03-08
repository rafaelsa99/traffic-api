from django.contrib.gis.db import models

class TrafficIntensity(models.Model):
    """
    Model representing traffic intensities bounded by a range of average speeds.
    """
    min_threshold = models.DecimalField(verbose_name='Minimum Threshold', max_digits=10, decimal_places=3)
    max_threshold = models.DecimalField(verbose_name='Maximum Threshold', max_digits=10, decimal_places=3)
    intensity = models.IntegerField()

    def __str__(self):
        return '{0} ({1}, {2})'.format(self.intensity, self.min_threshold, self.max_threshold)

    class Meta:
        verbose_name_plural = 'Traffic intensities'

class TrafficCharacterization(models.Model):
    """
    Model representing the characterization of traffic according to its intensity.
    """
    intensity = models.ForeignKey(TrafficIntensity, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class RoadSegment(models.Model):
    """
    Model for road segments, represented geographically by a line.
    """
    location = models.LineStringField(srid=4326)
    length = models.DecimalField(max_digits=10, decimal_places=3)
    characterization = models.ForeignKey(TrafficCharacterization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.location.geojson)

class Measurement(models.Model):
    """
    Model for the average speed measurements of road segments at a given instant.
    """
    segment = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    avg_speed = models.DecimalField(verbose_name='Average Speed', max_digits=10, decimal_places=3)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.avg_speed)

  