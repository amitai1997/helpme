from django.contrib.gis.db import models as gis_models
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

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


class EmergencyType(models.Model):
    EMERGENCY_CHOICES = [
        ("Medical", "Medical"),
        ("Fire", "Fire"),
        ("Police", "Police"),
        ("Road Assistance", "Road Assistance"),
        ("Natural Disaster", "Natural Disaster"),
        ("Vehicle Accident", "Vehicle Accident"),
        ("Lost Person", "Lost Person"),
        ("Intruder Alert", "Intruder Alert"),
        ("Gas Leak", "Gas Leak"),
        ("Animal Control", "Animal Control"),
        ("Child Abduction", "Child Abduction"),
        ("Domestic Violence", "Domestic Violence"),
        ("Water Rescue", "Water Rescue"),
        ("Mountain Rescue", "Mountain Rescue"),
        ("Mental Health Crisis", "Mental Health Crisis"),
        ("Terrorism", "Terrorism"),
        ("Hazmat Incident", "Hazmat Incident"),
        ("Power Outage", "Power Outage"),
        ("Environmental Hazard", "Environmental Hazard"),
        ("Civil Unrest", "Civil Unrest"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=50, choices=EMERGENCY_CHOICES, unique=True)

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=EmergencyType)
def remove_skills_from_volunteers(sender, instance, **kwargs):
    # Remove the skills from all volunteers associated with this EmergencyType
    for volunteer in Volunteer.objects.filter(skills=instance):
        volunteer.skills.remove(instance)


class EmergencyCall(models.Model):
    title = models.CharField(max_length=20, null=True)
    location = gis_models.PointField(geography=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUSES = [("Pending", "Pending"), ("Resolved", "Resolved")]
    status = models.CharField(max_length=20, choices=STATUSES, default="Pending")
    emergency_types = models.ManyToManyField(EmergencyType, related_name="emergency_calls")

    def __str__(self):
        return f"Emergency Call by {self.user.name}"


class Notification(models.Model):
    emergency_call = models.ForeignKey(
        EmergencyCall, on_delete=models.CASCADE, related_name="notifications", null=True
    )
    receivers = models.ManyToManyField(User, related_name="notifications_received")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.emergency_call} emergency"

    class Meta:
        ordering = ["-timestamp"]


class RescueTeam(models.Model):
    name = models.CharField(max_length=255)
    team_leader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    contact_information = models.TextField()

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = gis_models.PointField(geography=True, null=True, blank=True)
    skills = models.ManyToManyField(EmergencyType, related_name="skilled_volunteers")
    availability_status = models.BooleanField(default=True)
    contact_information = models.TextField()

    def __str__(self):
        return f"Volunteer: {self.user.name}"


class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    location = gis_models.PointField(geography=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location of {self.user.name}"
