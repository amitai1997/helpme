# signals.py in your app
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpme.emergency.models import EmergencyCall
from helpme.emergency.tasks import find_matching_volunteers, send_notifications


@receiver(post_save, sender=EmergencyCall)
def handle_emergency_call_creation(sender, instance, created, **kwargs):
    if created:
        # When an emergency call is created, trigger the Celery tasks
        # schedule_emergency_tasks.delay(instance.to_json())
        schedule_emergency_tasks(instance.to_json())


@shared_task
def schedule_emergency_tasks(emergency_call_json):
    # matching_volunteers = find_matching_volunteers.apply_async((instance,))
    # send_notifications.apply_async((matching_volunteers.get(), instance))
    matching_volunteers = find_matching_volunteers(emergency_call_json)
    send_notifications(matching_volunteers, emergency_call_json)
