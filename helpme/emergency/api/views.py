from rest_framework import viewsets

from helpme.emergency.models import (
    EmergencyCall,
    EmergencyType,
    Notification,
    Profile,
    RescueTeam,
    UserLocation,
    Volunteer,
)

from .serializers import (
    EmergencyCallSerializer,
    EmergencyTypeSerializer,
    NotificationSerializer,
    ProfileSerializer,
    RescueTeamSerializer,
    UserLocationSerializer,
    VolunteerSerializer,
)


# EmergencyCall view
class EmergencyCallViewSet(viewsets.ModelViewSet):
    queryset = EmergencyCall.objects.all()
    serializer_class = EmergencyCallSerializer


# Volunteer view
class VolunteerViewSet(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer


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


# UserProfile view
class EmergencyTypeViewSet(viewsets.ModelViewSet):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergencyTypeSerializer
