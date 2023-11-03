from django.contrib.gis.geos import Point
from rest_framework import serializers
from star_ratings.models import Rating

from helpme.emergency.models import (
    EmergencyCall,
    EmergencyType,
    Notification,
    Profile,
    RescueTeam,
    UserLocation,
    Volunteer,
)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"  # Include all fields from the Rating model


class LocationPointField(serializers.Field):
    def to_internal_value(self, data):
        try:
            latitude, longitude = map(float, data.split(","))
            if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                raise serializers.ValidationError("Invalid latitude or longitude values.")
            return Point(longitude, latitude)
        except (ValueError, AttributeError):
            raise serializers.ValidationError("Invalid location format.")

    def to_representation(self, value):
        if value is None:
            return None
        return f"{value.y},{value.x}"


class EmergencyCallSerializer(serializers.ModelSerializer):
    location = LocationPointField()

    class Meta:
        model = EmergencyCall
        fields = "__all__"


class VolunteerSerializer(serializers.ModelSerializer):
    location = LocationPointField()
    rating = RatingSerializer()

    class Meta:
        model = Volunteer
        fields = "__all__"


class RescueTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RescueTeam
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def validate_identification_number(self, value):
        # Add custom validation logic for identification_number
        if not value.isnumeric() or len(value) < 5:
            raise serializers.ValidationError("Invalid identification number.")
        return value

    def validate_gender(self, value):
        # Add custom validation logic for gender
        valid_genders = ["male", "female"]
        if value.lower() not in valid_genders:
            raise serializers.ValidationError("Invalid gender.")
        return value

    def validate_city(self, value):
        # Add custom validation logic for city
        if len(value) < 2:
            raise serializers.ValidationError("City name is too short.")
        return value


class EmergencyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyType
        fields = "__all__"
