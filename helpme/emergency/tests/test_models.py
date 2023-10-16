from django.contrib.gis.geos import Point
from django.test import TestCase

from helpme.emergency.models import EmergencyCall, Notification, RescueTeam, UserLocation, Volunteer
from helpme.users.models import User


class ModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            name="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

    def test_custom_user_creation(self):
        user = User.objects.get(email="testuser@example.com")
        self.assertEqual(user.name, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

    def test_emergency_call_creation(self):
        call = EmergencyCall.objects.create(
            location=Point(12.9716, 77.5946),
            description="Emergency at location",
            user=self.user,
            status="pending",
        )
        self.assertEqual(call.description, "Emergency at location")
        self.assertEqual(call.status, "pending")

    def test_volunteer_creation(self):
        volunteer = Volunteer.objects.create(
            user=self.user,
            location=Point(12.9716, 77.5946),
            skills="First Aid, CPR",
            availability_status=True,
            contact_information="volunteer@example.com",
        )
        self.assertEqual(volunteer.skills, "First Aid, CPR")
        self.assertTrue(volunteer.availability_status)

    def test_rescue_team_creation(self):
        team = RescueTeam.objects.create(
            name="Rescue Team 1",
            team_leader=self.user,
            contact_information="team@example.com",
        )
        self.assertEqual(team.name, "Rescue Team 1")
        self.assertEqual(team.team_leader, self.user)

    def test_notification_creation(self):
        notification = Notification.objects.create(
            message="Emergency call update",
            receiver=self.user,
            related_call=None,
        )
        self.assertEqual(notification.message, "Emergency call update")
        self.assertEqual(notification.receiver, self.user)

    def test_user_location_creation(self):
        location = UserLocation.objects.create(
            user=self.user,
            location=Point(12.9716, 77.5946),
        )
        self.assertEqual(location.user, self.user)
        self.assertEqual(location.location.x, 12.9716)
        self.assertEqual(location.location.y, 77.5946)
