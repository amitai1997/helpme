from time import sleep

from celery import shared_task

# from django.db.models import F, Q
from django.contrib.gis.db.models.functions import Distance
from django.core import serializers
from django.core.mail import send_mail
from django.db import transaction

from helpme.emergency.models import EmergencyCall, Notification, Volunteer


def find_matching_volunteers(emergency_call_json):
    emergency_call = EmergencyCall.from_json(emergency_call_json)
    # Extract location and required skills from the emergency call (you need to implement this part)
    required_location = emergency_call.location
    # required_skills = emergency_call.emergency_types.all()

    matched_volunteers = (
        Volunteer.objects.annotate(distance=Distance("location", required_location))
        .filter(distance__lte=100 * 1000)
        .order_by("distance")
    )

    # return matched_volunteers
    matching_volunteers_json = serializers.serialize("json", matched_volunteers)
    return matching_volunteers_json


@shared_task()
def send_notifications(matching_volunteers_json, emergency_call_json):
    matching_volunteers_data = serializers.deserialize("json", matching_volunteers_json, ignorenonexistent=True)
    matching_volunteers = [item.object for item in matching_volunteers_data]
    matching_users = [volunteer.user for volunteer in matching_volunteers]

    emergency_call = EmergencyCall.from_json(emergency_call_json)
    # Implement the logic to create notifications and send them to matching volunteers

    with transaction.atomic():
        emergency_call.save()
        sleep(1)
        notification = Notification.objects.create(
            emergency_call=emergency_call,
        )

    for user in matching_users:
        notification.receivers.add(user)

    for volunteer in matching_volunteers:
        send_notification_email.delay(volunteer.user.email, emergency_call_json)


@shared_task()
def send_notification_email(email_address, emergency_call_json):
    emergency_call = EmergencyCall.from_json(emergency_call_json)
    try:
        sleep(15)  # Simulate expensive operation(s) that freeze Django
        send_mail(
            f"{emergency_call.title}",
            f"\t{emergency_call.description}\n\nThank you!",
            "support@helpme.co.il",
            [email_address],
            fail_silently=False,
        )
        return {"success": True, "message": "Email sent successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
