from django.contrib.gis.geos import Point
from django.test import TestCase

from helpme.users.models import Location, User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.pk}/"


class LocationTestCase(TestCase):
    def setUp(self):
        # Create sample Location instances for testing
        self.location1 = Location.objects.create(name="Location 1", geometry=Point(1, 1))
        self.location2 = Location.objects.create(name="Location 2", geometry=Point(2, 2))

    def tearDown(self):
        # Clean up the test data
        self.location1.delete()
        self.location2.delete()

    def test_location_creation(self):
        # Test if the Location instances were created correctly
        self.assertEqual(self.location1.name, "Location 1")
        self.assertEqual(self.location1.geometry, Point(1, 1))
        self.assertEqual(self.location2.name, "Location 2")
        self.assertEqual(self.location2.geometry, Point(2, 2))

    def test_location_str_method(self):
        # Test the __str__ method of the Location model
        self.assertEqual(str(self.location1), "Location 1 (1.000000, 1.000000)")
        self.assertEqual(str(self.location2), "Location 2 (2.000000, 2.000000)")

    def test_location_query(self):
        # Test querying for Location objects
        locations = Location.objects.filter(name="Location 1")
        self.assertEqual(locations.count(), 1)
        self.assertEqual(locations[0], self.location1)
