# signals.py in your app
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpme.emergency.models import Profile
from helpme.users.models import User


@receiver(post_save, sender=User, dispatch_uid="handle_User_creation_signal")
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.
    """
    if created:
        # Check if a profile for the user already exists
        if not Profile.objects.filter(user=instance).exists():
            # Create a new profile for the user
            Profile.objects.create(user=instance)
