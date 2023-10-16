from rest_framework import serializers

from helpme.emergency.models import EmergencyCall, Notification, RescueTeam, UserLocation, Volunteer


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
