from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ValidationError, ModelSerializer, Serializer, FileField, StringRelatedField, EmailField, CharField
from .models import RoadSegment, Measurement
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User, Group

class FileUploadSerializer(Serializer):
    """
    Serializer class to upload a file.
    """
    file = FileField()

class RoadSegmentSerializer(GeoFeatureModelSerializer):
    """
    Serializer class for road segments.
    """
    characterization = StringRelatedField()
    class Meta:
        model = RoadSegment
        geo_field = "location"
        fields = ['id', 'length', 'characterization']

class MeasurementSerializer(ModelSerializer):
    """
    Serializer class for speed measurements.
    """
    class Meta:
        model = Measurement
        fields = ['id', 'segment', 'avg_speed', 'created_on']

class GroupSerializer(ModelSerializer):
    """
    Serializer class for user groups.
    """
    class Meta:
        model = Group
        fields = ['id', 'name']

class RegisterUserSerializer(ModelSerializer):
    """
    Serializer class for register new users.
    """
    email = EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = CharField(write_only=True, required=True, validators=[validate_password])
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'groups')

    def validate(self, attrs):
        """
        Check if both password fields contains the same value.
        """
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        """
        Register the new user and assign the given groups.
        """
        groups_data = validated_data.pop('groups')
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        for group_data in groups_data:
            user.groups.add(group_data)
        return user