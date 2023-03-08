from rest_framework import viewsets, status, permissions, generics, response
from rest_framework.views import APIView
from .models import RoadSegment, Measurement, TrafficIntensity, TrafficCharacterization
from .serializers import GroupSerializer, RoadSegmentSerializer, MeasurementSerializer, FileUploadSerializer, RegisterUserSerializer
from django.contrib.gis.geos import LineString
from .permissions import CanCRUD, CanRead
import pandas as pd
from django.contrib.auth.models import Group

def update_segment_characterization(segment, speed):
    """"
    Helper method to update the characterization of a given road segment with a given average spee.
    """
    intensity = TrafficIntensity.objects.get(min_threshold__lte=speed, max_threshold__gte=speed)
    characterization = TrafficCharacterization.objects.get(intensity=intensity)
    road = RoadSegment.objects.get(id=segment)
    road.characterization = characterization
    road.save()

class UploadFileView(generics.CreateAPIView):
    """
    API endpoint to upload data through a CSV file.
    """

    serializer_class = FileUploadSerializer

    def post(self, request):
        """
        Reads the given CSV file and inserts the data to the database.
        """
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
    queryset = RoadSegment.objects.all().order_by('-characterization')
    serializer_class = RoadSegmentSerializer
    filterset_fields = ('characterization',)
    
    def get_permissions(self):
        """
        Define the permissions according to the type of request.
        """    
        if self.request.method == 'GET':
            self.permission_classes = [CanRead]
        elif self.request.method == 'POST' or self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CanCRUD]
        return super(RoadSegmentViewSet, self).get_permissions()


class MeasurementView(APIView):
    """
    API endpoint that allows read and create measurements for a given road segment.
    """

    def get_permissions(self):  
        """
        Define the permissions according to the type of request.
        """      
        if self.request.method == 'GET':
            self.permission_classes = [CanRead]
        elif self.request.method == 'POST' or self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CanCRUD]
        return super(MeasurementView, self).get_permissions()

    def get(self, request, *args, **kwargs):
        """
        List all the measurements for a given road segment.
        """
        segment = kwargs.pop('segment')
        measurements = Measurement.objects.filter(segment = segment).order_by('-created_on')
        serializer = MeasurementSerializer(measurements, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a measurement for a road segment with an average speed.
        Updates the characterization of the road segment accordingly.
        """
        data = {
            'avg_speed': round(request.data.get('avg_speed'), 3),
            'segment': kwargs.pop('segment')
        }
        serializer = MeasurementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # Updates the road segment characterization
            update_segment_characterization(data["segment"], data["avg_speed"])
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeasurementDetailView(APIView):
    """
    API endpoint that allows to read, update and delete a given measurement.
    """

    def get_permissions(self):  
        """
        Define the permissions according to the type of request.
        """      
        if self.request.method == 'GET':
            self.permission_classes = [CanRead]
        elif self.request.method == 'POST' or self.request.method == 'DELETE' or self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CanCRUD]
        return super(MeasurementDetailView, self).get_permissions()

    def get_measurement(self, measurement_id):
        '''
        Helper method to get the measurement object with a given id.
        '''
        try:
            return Measurement.objects.get(id=measurement_id)
        except Measurement.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        '''
        Retrieves the measurement with a given id.
        '''
        instance = self.get_measurement(kwargs.pop('measurement'))
        if not instance:
            return response.Response(
                {"res": "Measurement with given id does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MeasurementSerializer(instance)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        '''
        Updates a measurement with a given id.
        '''
        instance = self.get_measurement(kwargs.pop('measurement'))
        if not instance:
            return response.Response(
                {"res": "Measurement with given id does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'avg_speed': request.data.get('avg_speed'), 
        }
        serializer = MeasurementSerializer(instance = instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            update_segment_characterization(kwargs.pop('segment'), data["avg_speed"])
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        '''
        Deletes a measurement with a given id.
        '''
        instance = self.get_measurement(kwargs.pop('measurement'))
        if not instance:
            return response.Response(
                {"res": "Measurement with given id does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return response.Response(
            {"res": "Measurement deleted!"},
            status=status.HTTP_200_OK
        )

class RegisterUserView(generics.CreateAPIView):
    """
    API endpoint to register a user.
    """
    serializer_class = RegisterUserSerializer
    permission_classes = [CanCRUD]

class GroupView(generics.ListAPIView):
    """
    API endpoint to list user groups.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [CanCRUD]