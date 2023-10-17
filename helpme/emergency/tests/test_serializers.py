from rest_framework.test import APITestCase

from helpme.emergency.api.serializers import ProfileSerializer
from helpme.emergency.models import Profile
from helpme.users.models import User


class ProfileSerializerTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            name="testuser",
            email="testuser@example.com",
            password="testpassword",
        )

    def test_valid_serializer_data(self):
        user = User.objects.get(email="testuser@example.com")
        data = {
            "user": user.pk,
            "identification_number": "12345",
            "gender": "Male",
            "date_of_birth": "1990-01-01",
            "city": "New York",
            "preferred_area": "North",
            "carrying_weapon": False,
            "driving_license_tractor": True,
        }
        serializer = ProfileSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        profile = Profile.objects.create(**data)
        return profile

    def test_invalid_identification_number(self):
        data = {
            "user": 1,
            "identification_number": "abc",  # Invalid identification_number
            "gender": "male",
            "date_of_birth": "1990-01-01",
            "city": "New York",
            "preferred_area": "North",
            "carrying_weapon": False,
            "driving_license_tractor": True,
        }
        serializer = ProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_gender(self):
        data = {
            "user": 1,
            "identification_number": "12345",
            "gender": "unknown",  # Invalid gender
            "date_of_birth": "1990-01-01",
            "city": "New York",
            "preferred_area": "North",
            "carrying_weapon": False,
            "driving_license_tractor": True,
        }
        serializer = ProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_city(self):
        data = {
            "user": 1,
            "identification_number": "12345",
            "gender": "male",
            "date_of_birth": "1990-01-01",
            "city": "N",  # Invalid city
            "preferred_area": "North",
            "carrying_weapon": False,
            "driving_license_tractor": True,
        }
        serializer = ProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())
