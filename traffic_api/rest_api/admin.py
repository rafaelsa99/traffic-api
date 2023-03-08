from django.contrib.gis import admin
from .models import TrafficCharacterization, TrafficIntensity, RoadSegment, Measurement

admin.site.register(TrafficIntensity)
admin.site.register(TrafficCharacterization)
admin.site.register(RoadSegment)
admin.site.register(Measurement)
