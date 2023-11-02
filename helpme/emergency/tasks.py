# tasks.py
import logging
import random
from time import sleep

from celery import shared_task
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Count

from helpme.emergency.api.views import validate_location
from helpme.emergency.models import EmergencyCall, Notification, Volunteer

logger = logging.getLogger(__name__)


@shared_task
def process_emergency_call(emergency_call_id):
    """
    Process an emergency call asynchronously.

    Args:
        emergency_call_id (int): The ID of the emergency call to process.

    Returns:
        Any: Result of the processing.
    """
    try:
        emergency_call = EmergencyCall.objects.get(id=emergency_call_id)

        result = (
            find_matching_volunteers.s(EmergencyCall.to_json(emergency_call))
            | send_notifications.s(emergency_call.id)
            | send_notification_email.s(emergency_call.id)
        )()
        return result
    except Exception as e:
        logger.error(f"Error processing emergency call: {e}")
        return None


@shared_task
def find_matching_volunteers(emergency_call_json):
    """
    Find matching volunteers for an emergency call.

    Args:
        emergency_call_json (str): JSON representation of the emergency call.

    Returns:
        str: JSON representation of matching volunteers.
    """
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
        logger.error(f"Error finding matching volunteers: {e}")
        return None


@shared_task()
def send_notifications(matching_volunteers_json, emergency_call_id):
    """
    Send notifications to matching volunteers.

    Args:
        matching_volunteers_json (str): JSON representation of matching volunteers.
        emergency_call_id (int): The ID of the emergency call.

    Returns:
        str: JSON representation of matching users.
    """
    try:
        emergency_call = EmergencyCall.objects.get(id=emergency_call_id)

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
        logger.error(f"Error sending notifications: {e}")
        return None


@shared_task()
def send_notification_email(matching_users_json, emergency_call_id):
    """
    Send email notifications to matching users.

    Args:
        matching_users_json (str): JSON representation of matching users.
        emergency_call_id (int): The ID of the emergency call.

    Returns:
        dict: A dictionary indicating the result of the email notifications.
    """
    try:
        emergency_call = EmergencyCall.objects.get(id=emergency_call_id)
        matching_users_data = serializers.deserialize("json", matching_users_json, ignorenonexistent=True)
        matching_users = [item.object for item in matching_users_data]

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
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        logger.error(f"Error sending email notifications: {e}")
        return None


@shared_task
def update_locations():
    logging.info("Update locations task is running")
    volunteers = Volunteer.objects.all()

    for volunteer in volunteers:
        # Simulate random location updates
        new_location = Point(
            x=volunteer.location.x + random.uniform(-0.01, 0.01),
            y=volunteer.location.y + random.uniform(-0.01, 0.01),
        )

        # Call the location validation function
        error_message = "Invalid location"
        response = validate_location(None, new_location, error_message)
        if response:
            # Invalid location, handle the response as needed (e.g., log it)
            continue

        volunteer.location = new_location
        volunteer.save()

    logging.info("Update locations task completed")
