import logging
from time import sleep

from celery import shared_task
from django.contrib.gis.db.models.functions import Distance
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Count

from helpme.emergency.models import EmergencyCall, Notification, Volunteer

logger = logging.getLogger(__name__)


@shared_task
def process_emergency_call(emergency_call_id):
    emergency_call = EmergencyCall.objects.get(id=emergency_call_id)

    result = (
        find_matching_volunteers.s(EmergencyCall.to_json(emergency_call))
        | send_notifications.s(emergency_call.id)
        | send_notification_email.s(emergency_call.id)
    )()
    return result


@shared_task
def find_matching_volunteers(emergency_call_json):
    try:
        emergency_call = EmergencyCall.from_json(emergency_call_json)

        required_location = emergency_call.location
        required_skills = emergency_call.emergency_types.all()

        # Calculate the distance between each volunteer's location and the required location
        matched_volunteers = (
            Volunteer.objects.annotate(distance=Distance("location", required_location))
            .filter(
                distance__lte=100 * 10000, skills__in=required_skills
            )  # 100 km in meters  # Filter by shared skills
            .annotate(skill_count=Count("skills"))  # Count the number of shared skills
            .filter(skill_count__gt=0)  # Filter volunteers with at least one shared skill
            .filter(availability_status=True)
        )

        # Serialize the matched volunteers to JSON
        matching_volunteers_json = serializers.serialize("json", matched_volunteers)
        return matching_volunteers_json

    except Exception as e:
        logger.error(e)
        return None  #


@shared_task()
def send_notifications(matching_volunteers_json, emergency_call_id):
    emergency_call = EmergencyCall.objects.get(id=emergency_call_id)
    try:
        # Deserialize JSON data to obtain matching volunteer objects
        matching_volunteers_data = serializers.deserialize("json", matching_volunteers_json, ignorenonexistent=True)
        matching_volunteers = [item.object for item in matching_volunteers_data]

        # Extract user objects from matching volunteers
        matching_users = [volunteer.profile.user for volunteer in matching_volunteers]

        # Create a notification for the emergency call
        notification = Notification.objects.create(
            emergency_call=emergency_call,
        )

        # Add matching users as receivers of the notification
        for user in matching_users:
            notification.receivers.add(user)

        matching_users_json = serializers.serialize("json", matching_users)
        return matching_users_json

    except Exception as e:
        logger.error(e)
        return None  # Return None or another error indicator


@shared_task()
def send_notification_email(matching_users_json, emergency_call_id):
    emergency_call = EmergencyCall.objects.get(id=emergency_call_id)
    matching_users_data = serializers.deserialize("json", matching_users_json, ignorenonexistent=True)
    matching_users = [item.object for item in matching_users_data]

    try:
        # Send notification emails to matching volunteers
        for user in matching_users:
            # Simulate an expensive operation that takes 7 seconds
            sleep(7)

            # Send an email notification to the provided email address
            send_mail(
                f"Notification: {emergency_call.title}",
                f"{emergency_call.description}\n\nThank you!",
                "support@helpme.co.il",
                [user.email],
                fail_silently=False,
            )

        # Return a success message if the email is sent successfully
        return {"success": True, "message": "Email sent successfully."}

    except Exception as e:
        logger.error(e)
        return None
