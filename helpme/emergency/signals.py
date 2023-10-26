# signals.py in your app
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from helpme.emergency.models import EmergencyCall
from helpme.emergency.tasks import schedule_emergency_tasks

# @receiver(post_save, sender=EmergencyCall, dispatch_uid="handle_emergency_call_creation_signal")
# @receiver(m2m_changed, sender=EmergencyCall.emergency_types.through)
# def handle_emergency_call_creation(sender, instance, created, **kwargs):
#     if created:
#         schedule_emergency_tasks(instance.id)


@receiver(m2m_changed, sender=EmergencyCall.emergency_types.through)
def handle_emergency_types_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        # This signal is triggered after new emergency types are added to the EmergencyCall
        # You can access the updated instance with the populated emergency types here
        schedule_emergency_tasks(instance.id)
