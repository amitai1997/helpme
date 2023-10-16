from django.contrib.gis.db import models as gis_models

# from django.contrib.gis.geos import Point
from django.db import models

from helpme.users.models import User


class EmergencyCall(models.Model):
    location = gis_models.PointField(geography=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Emergency Call by {self.user.username}"


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    skills = models.TextField()
    availability_status = models.BooleanField(default=True)
    contact_information = models.TextField()

    def __str__(self):
        return f"Volunteer: {self.user.username}"


class RescueTeam(models.Model):
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_information = models.TextField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    related_call = models.ForeignKey(EmergencyCall, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification to {self.receiver.username}"


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = gis_models.PointField(geography=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location of {self.user.username}"
