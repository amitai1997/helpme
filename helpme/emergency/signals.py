# signals.py in your app
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpme.emergency.models import EmergencyCall
from helpme.emergency.tasks import schedule_emergency_tasks


@receiver(post_save, sender=EmergencyCall, dispatch_uid="handle_emergency_call_creation_signal")
def handle_emergency_call_creation(sender, instance, created, **kwargs):
    if created:
        schedule_emergency_tasks(instance.id)
