# from celery import shared_task
from time import sleep

from celery import shared_task
from django.contrib.gis.db.models.functions import Distance
from django.core.mail import send_mail
from django.db.models import Q

from config import celery_app
from helpme.emergency.models import Notification, Volunteer


# @shared_task
@celery_app.task()
def send_notifications(notification_content, volunteers):
    for volunteer in volunteers:
        notification = Notification(
            message=notification_content,
            receiver=volunteer,
            related_call=None,  # Set this based on the specific call
        )
        notification.save()

        # Send email notification
        # TODO send email push notification
        # response = send_email_notification(volunteer.email, notification_content)

        # if response.status_code == 200:
        # Email sent successfully, you can update the notification status here
        # pass


def match_volunteers(emergency_call):
    # Extract location and required skills from the emergency call (you need to implement this part)
    required_location = emergency_call.location
    required_skills = emergency_call.skills

    # Match volunteers based on location and skills
    matched_volunteers = Volunteer.objects.filter(
        Q(location__distance_lte=(required_location, Distance(km=10))) & Q(skills__icontains=required_skills)
    )

    return matched_volunteers


@shared_task()
def send_feedback_email_task(email_address, message):
    try:
        sleep(21)  # Simulate expensive operation(s) that freeze Django
        send_mail(
            "Your Feedback",
            f"\t{message}\n\nThank you!",
            "support@helpme.co.il",
            [email_address],
            fail_silently=False,
        )
        return {"success": True, "message": "Email sent successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
