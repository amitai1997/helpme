from django.contrib.gis.geos import Point
from django.test import TestCase

from helpme.emergency.models import EmergencyCall, Notification, Profile, RescueTeam, UserLocation, Volunteer
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


class ProfileModelTestCase(TestCase):
    def setUp(self):
        # Create a user and a profile for testing
        self.user = User.objects.create_user(email="testuser", name="testuser", password="testpassword")
        self.profile = Profile.objects.create(
            user=self.user,
            identification_number="123456789",
            gender="Male",
            date_of_birth="2000-01-01",
            city="TestCity",
            preferred_area="North",
            carrying_weapon=True,
            driving_license_tractor=False,
        )

    def test_profile_creation(self):
        # Test if the profile was created correctly
        self.assertEqual(self.profile.identification_number, "123456789")
        self.assertEqual(self.profile.gender, "Male")
        self.assertEqual(str(self.profile.date_of_birth), "2000-01-01")
        self.assertEqual(self.profile.city, "TestCity")
        self.assertEqual(self.profile.preferred_area, "North")
        self.assertTrue(self.profile.carrying_weapon)
        self.assertFalse(self.profile.driving_license_tractor)

    def test_profile_user_relation(self):
        # Test if the profile is associated with the correct user
        self.assertEqual(self.profile.user, self.user)

    def test_profile_str_representation(self):
        # Test the string representation of the profile
        expected_str = f"Profile for {self.user.name}"
        self.assertEqual(str(self.profile), expected_str)
