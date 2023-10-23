# from celery import shared_task
from time import sleep

from celery import shared_task

# from django.contrib.gis.db.models.functions import Distance
from django.core.mail import send_mail

# from config import celery_app
from helpme.emergency.models import EmergencyCall, Notification, Volunteer

# from django.db.models import F, Q


@shared_task()
def find_matching_volunteers(emergency_call_json):
    # emergency_call = EmergencyCall.from_json(emergency_call_json)
    # Extract location and required skills from the emergency call (you need to implement this part)
    # required_location = emergency_call.location
    # required_skills = emergency_call.emergency_types.all()

    # Match volunteers based on location and skills
    # matched_volunteers = Volunteer.objects.filter(
    #     Q(location__distance_lte=(Distance(F('location'), required_location), 1000)) & Q(skills__in=required_skills)
    #      skills__in=required_skills
    # )
    matched_volunteers = Volunteer.objects.all()

    return matched_volunteers


@shared_task()
def send_notifications(matching_volunteers, emergency_call_json):
    emergency_call = EmergencyCall.from_json(emergency_call_json)
    # Implement the logic to create notifications and send them to matching volunteers
    notification = Notification.objects.create(
        emergency_call=emergency_call,
    )

    existing_users = matching_volunteers.values_list("user", flat=True)
    # Create a notification
    notification.receivers.set(existing_users)

    for volunteer in matching_volunteers:
        # Implement the notification sending logic (e.g., email, SMS, push notifications)
        send_notification_email.delay(volunteer.user.email, emergency_call_json)


@shared_task()
def send_notification_email(email_address, emergency_call_json):
    emergency_call = EmergencyCall.from_json(emergency_call_json)
    try:
        sleep(3)  # Simulate expensive operation(s) that freeze Django
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
