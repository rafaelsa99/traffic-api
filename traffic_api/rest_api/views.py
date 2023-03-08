from rest_framework import viewsets, status, permissions, generics, response
from .models import RoadSegment, Measurement, TrafficIntensity, TrafficCharacterization
from .serializers import RoadSegmentSerializer, MeasurementSerializer, FileUploadSerializer
from django.contrib.gis.geos import LineString
import pandas as pd

class UploadFileView(generics.CreateAPIView):

    serializer_class = FileUploadSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file)
        for i,row in reader.iterrows():
            line = LineString((float(row['Long_start']), float(row['Lat_start'])), (float(row['Length']), float(row['Long_end'])))
            speed = round(row['Speed'], 3)
            intensity = TrafficIntensity.objects.get(min_threshold__lte=speed, max_threshold__gte=speed)
            characterization = TrafficCharacterization.objects.get(intensity=intensity)
            new_segment = RoadSegment(length = round(row['Lat_end'], 3), location = line, characterization=characterization)
            new_segment.save()
            new_measurement = Measurement(avg_speed=speed, segment=new_segment)
            new_measurement.save()
        return response.Response(status=status.HTTP_201_CREATED)

class RoadSegmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations on road segments.
    """
    queryset = RoadSegment.objects.all()
    serializer_class = RoadSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations on measurements.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]