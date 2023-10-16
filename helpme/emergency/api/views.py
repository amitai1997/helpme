from rest_framework import viewsets

from helpme.emergency.models import EmergencyCall, Notification, RescueTeam, UserLocation, Volunteer

from .serializers import (
    EmergencyCallSerializer,
    NotificationSerializer,
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
