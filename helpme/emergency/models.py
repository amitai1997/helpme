from django.contrib.gis.db import models as gis_models

# from django.contrib.gis.geos import Point
from django.db import models

from helpme.users.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification_number = models.CharField(max_length=20)
    GENDERS = [("Male", "Male"), ("Female", "Female")]
    gender = models.CharField(max_length=10, choices=GENDERS)
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100)
    PREFERRED_AREA_CHOICES = [
        ("North", "North"),
        ("South", "South"),
        ("Center", "Center"),
        ("Emek", "Emek"),
        ("Sharon", "Sharon"),
        ("Shfela", "Shfela"),
        ("Jerusalem", "Jerusalem"),
        ("Valley", "Valley"),
        ("Not Determined", "Not Determined"),
    ]
    preferred_area = models.CharField(max_length=20, choices=PREFERRED_AREA_CHOICES)
    carrying_weapon = models.BooleanField()
    driving_license_tractor = models.BooleanField()

    def save(self, *args, **kwargs):
        choice = self.preferred_area
        if not any(choice in _tuple for _tuple in self.PREFERRED_AREA_CHOICES):
            raise ValueError('Invalid "preferred_area" choice.')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile for {self.user.name}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    preferred_area__in=[
                        choice
                        for choice in [
                            "North",
                            "South",
                            "Center",
                            "Emek",
                            "Sharon",
                            "Shfela",
                            "Jerusalem",
                            "Valley",
                            "Not Determined",
                        ]
                    ]
                ),
                name="valid_preferred_area",
            )
        ]


class EmergencyCall(models.Model):
    location = gis_models.PointField(geography=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Emergency Call by {self.user.name}"


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    skills = models.TextField()
    availability_status = models.BooleanField(default=True)
    contact_information = models.TextField()

    def __str__(self):
        return f"Volunteer: {self.user.name}"


class RescueTeam(models.Model):
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    contact_information = models.TextField()

    def __str__(self):
        return self.name


class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    related_call = models.ForeignKey(EmergencyCall, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Notification to {self.receiver.name}"


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    location = gis_models.PointField(geography=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location of {self.user.name}"
