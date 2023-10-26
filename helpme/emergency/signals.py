# signals.py in your app
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpme.emergency.models import EmergencyCall
from helpme.emergency.tasks import find_matching_volunteers, send_notifications


@receiver(post_save, sender=EmergencyCall, dispatch_uid="handle_emergency_call_creation_signal")
def handle_emergency_call_creation(sender, instance, created, **kwargs):
    if created:
        schedule_emergency_tasks(instance.id)


@shared_task
def schedule_emergency_tasks(emergency_call_id):
    try:
        emergency_call = EmergencyCall.objects.get(id=emergency_call_id)
        matching_volunteers_json = find_matching_volunteers(emergency_call.to_json())
        send_notifications(matching_volunteers_json, emergency_call.to_json())
    except EmergencyCall.DoesNotExist:
        # Handle the case where the EmergencyCall doesn't exist
        pass
