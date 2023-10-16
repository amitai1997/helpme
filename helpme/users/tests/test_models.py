from helpme.users.models import User

# from django.test import TestCase


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.pk}/"
