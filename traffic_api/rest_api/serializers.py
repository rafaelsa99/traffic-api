from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer, Serializer, FileField, StringRelatedField
from .models import RoadSegment, Measurement

class FileUploadSerializer(Serializer):
    file = FileField()

class RoadSegmentSerializer(GeoFeatureModelSerializer):
    characterization = StringRelatedField()
    class Meta:
        model = RoadSegment
        geo_field = "location"
        fields = ['id', 'length', 'characterization']

class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['id', 'segment', 'avg_speed', 'created_on']