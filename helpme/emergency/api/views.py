from rest_framework import status, viewsets
from rest_framework.response import Response

from helpme.emergency.models import (
    EmergencyCall,
    EmergencyType,
    GeoJSONFeature,
    Notification,
    Profile,
    RescueTeam,
    UserLocation,
    Volunteer,
)

from .serializers import (
    EmergencyCallSerializer,
    EmergencyTypeSerializer,
    LocationPointField,
    NotificationSerializer,
    ProfileSerializer,
    RescueTeamSerializer,
    UserLocationSerializer,
    VolunteerSerializer,
)


def validate_location(request, location, error_message):
    is_within_permitted_location = GeoJSONFeature.objects.filter(geometry__contains=location).exists()
    if not is_within_permitted_location:
        return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
    return None


# EmergencyCall view
class EmergencyCallViewSet(viewsets.ModelViewSet):
    queryset = EmergencyCall.objects.all()
    serializer_class = EmergencyCallSerializer

    def create(self, request, *args, **kwargs):
        location = LocationPointField.to_internal_value(self, request.data["location"])
        error_response = validate_location(request, location, "Emergency call location is not within permitted areas.")
        if error_response:
            return error_response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"message": "Emergency call created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED
        )


# Volunteer view
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

    def create(self, request, *args, **kwargs):
        location = LocationPointField.to_internal_value(self, request.data["location"])
        error_response = validate_location(request, location, "Volunteer location is not within permitted areas.")
        if error_response:
            return error_response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"message": "Volunteer created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED
        )


# RescueTeam view (optional)
class RescueTeamViewSet(viewsets.ModelViewSet):
    queryset = RescueTeam.objects.all()
    serializer_class = RescueTeamSerializer


# Notification view
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


# UserLocation view
class UserLocationViewSet(viewsets.ModelViewSet):
    queryset = UserLocation.objects.all()
    serializer_class = UserLocationSerializer


# UserProfile view
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# Emergencytype view
class EmergencyTypeViewSet(viewsets.ModelViewSet):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer
