from rest_framework import serializers

from helpme.emergency.models import EmergencyCall, Notification, Profile, RescueTeam, UserLocation, Volunteer


class EmergencyCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyCall
        fields = "__all__"


class VolunteerSerializer(serializers.ModelSerializer):
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
