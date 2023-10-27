from time import sleep

from celery import shared_task
from django.contrib.gis.db.models.functions import Distance
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Count

from helpme.emergency.models import EmergencyCall, Notification, Volunteer


@shared_task
def schedule_emergency_tasks(emergency_call_id):
    try:
        emergency_call = EmergencyCall.objects.get(id=emergency_call_id)
        matching_volunteers_json = find_matching_volunteers(emergency_call)
        send_notifications(matching_volunteers_json, emergency_call.to_json())
    except EmergencyCall.DoesNotExist:
        # Handle the case where the EmergencyCall doesn't exist
        # Log the error and possibly notify administrators
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"EmergencyCall with ID {emergency_call_id} does not exist.")
        # You can also notify administrators or take other appropriate actions

    except Exception as e:
        # Handle other exceptions that may occur during the task execution
        # Log the error and possibly notify administrators
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"An error occurred while processing the task: {str(e)}")
        # You can also notify administrators or take other appropriate actions


def find_matching_volunteers(emergency_call):
    # Extract the required location and skills from the emergency call
    required_location = emergency_call.location
    required_skills = emergency_call.emergency_types.all()

    # Calculate the distance between each volunteer's location and the required location
    matched_volunteers = (
        Volunteer.objects.annotate(distance=Distance("location", required_location))
        .filter(distance__lte=100 * 10000, skills__in=required_skills)  # 100 km in meters  # Filter by shared skills
        .annotate(skill_count=Count("skills"))  # Count the number of shared skills
        .filter(skill_count__gt=0)  # Filter volunteers with at least one shared skill
        .filter(availability_status=True)
    )

    # Serialize the matched volunteers to JSON
    matching_volunteers_json = serializers.serialize("json", matched_volunteers)

    return matching_volunteers_json


@shared_task()
def send_notifications(matching_volunteers_json, emergency_call_json):
    # Deserialize JSON data to obtain matching volunteer objects
    matching_volunteers_data = serializers.deserialize("json", matching_volunteers_json, ignorenonexistent=True)
    matching_volunteers = [item.object for item in matching_volunteers_data]

    # Extract user objects from matching volunteers
    matching_users = [volunteer.profile.user for volunteer in matching_volunteers]

    # Deserialize the emergency call JSON to get the emergency call object
    emergency_call = EmergencyCall.from_json(emergency_call_json)

    # Create a notification for the emergency call
    notification = Notification.objects.create(
        emergency_call=emergency_call,
    )

    # Add matching users as receivers of the notification
    for user in matching_users:
        notification.receivers.add(user)

    # Send notification emails to matching volunteers
    for volunteer in matching_volunteers:
        send_notification_email.delay(volunteer.profile.user.email, emergency_call_json)


@shared_task()
def send_notification_email(email_address, emergency_call_json):
    # Deserialize the emergency call JSON to get the emergency call object
    emergency_call = EmergencyCall.from_json(emergency_call_json)

    try:
        # Simulate an expensive operation that takes 7 seconds
        sleep(7)

        # Send an email notification to the provided email address
        send_mail(
            f"Notification: {emergency_call.title}",
            f"{emergency_call.description}\n\nThank you!",
            "support@helpme.co.il",
            [email_address],
            fail_silently=False,
        )

        # Return a success message if the email is sent successfully
        return {"success": True, "message": "Email sent successfully."}

    except Exception as e:
        # Handle exceptions that may occur during email sending
        # Return an error message with details if an exception is raised
        return {"success": False, "error": str(e)}
