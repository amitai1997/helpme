# from django.shortcuts import render
from time import sleep

from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.views import View

# from helpme.emergency.tasks import send_notifications


class SendEmailView(View):
    def get(self, request):
        """Sends an email when the feedback form has been submitted."""
        try:
            # Get data from the request object
            message = request.GET.get("message", "")
            email_address = request.GET.get("email_address", "")

            # Simulate expensive operation(s) with sleep
            sleep(20)

            # Send email
            send_mail(
                "Your Feedback",
                f"\t{message}\n\nThank you!",
                "support@example.com",
                [email_address],
                fail_silently=False,
            )

            return JsonResponse({"message": "Email sent successfully!."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
